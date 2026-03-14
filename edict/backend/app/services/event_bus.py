"""Redis Streams 事件总线 — 可靠的事件发布/消费。

核心能力：
- publish: XADD 发布事件到 stream
- subscribe: XREADGROUP 消费者组消费，带 ACK 保证
- 未 ACK 的事件在消费者崩溃后会被自动重新投递
- 解决旧架构 daemon 线程丢失导致派发永久中断的根因
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any

import redis.asyncio as aioredis

from ..config import get_settings

log = logging.getLogger("edict.event_bus")

# ── 标准 Topic 常量 ──
TOPIC_TASK_CREATED = "task.created"
TOPIC_TASK_PLANNING_REQUEST = "task.planning.request"
TOPIC_TASK_PLANNING_COMPLETE = "task.planning.complete"
TOPIC_TASK_REVIEW_REQUEST = "task.review.request"
TOPIC_TASK_REVIEW_RESULT = "task.review.result"
TOPIC_TASK_DISPATCH = "task.dispatch"
TOPIC_TASK_STATUS = "task.status"
TOPIC_TASK_COMPLETED = "task.completed"
TOPIC_TASK_CLOSED = "task.closed"
TOPIC_TASK_REPLAN = "task.replan"
TOPIC_TASK_STALLED = "task.stalled"
TOPIC_TASK_ESCALATED = "task.escalated"

TOPIC_AGENT_THOUGHTS = "agent.thoughts"
TOPIC_AGENT_TODO_UPDATE = "agent.todo.update"
TOPIC_AGENT_HEARTBEAT = "agent.heartbeat"

# 所有 topic 对应的 Redis Stream key 前缀
STREAM_PREFIX = "edict:stream:"


class EventBus:
    """Redis Streams 事件总线。"""

    def __init__(self, redis_url: str | None = None):
        self._redis_url = redis_url or get_settings().redis_url
        self._redis: aioredis.Redis | None = None

    async def connect(self):
        """建立 Redis 连接。"""
        if self._redis is None:
            self._redis = aioredis.from_url(
                self._redis_url,
                decode_responses=True,
                max_connections=20,
            )
            log.info(f"EventBus connected to Redis: {self._redis_url}")

    async def close(self):
        if self._redis:
            await self._redis.aclose()
            self._redis = None

    @property
    def redis(self) -> aioredis.Redis:
        assert self._redis is not None, "EventBus not connected. Call connect() first."
        return self._redis

    def _stream_key(self, topic: str) -> str:
        return f"{STREAM_PREFIX}{topic}"

    async def publish(
        self,
        topic: str,
        trace_id: str,
        event_type: str,
        producer: str,
        payload: dict[str, Any] | None = None,
        meta: dict[str, Any] | None = None,
    ) -> str:
        """发布事件到 Redis Stream。

        Returns:
            event_id (str): 由 Redis 自动生成的 Stream entry ID
        """
        event = {
            "event_id": str(uuid.uuid4()),
            "trace_id": trace_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "topic": topic,
            "event_type": event_type,
            "producer": producer,
            "payload": json.dumps(payload or {}, ensure_ascii=False),
            "meta": json.dumps(meta or {}, ensure_ascii=False),
        }
        stream_key = self._stream_key(topic)
        entry_id = await self.redis.xadd(stream_key, event, maxlen=10000)
        log.debug(f"📤 Published {topic}/{event_type} → {stream_key} [{entry_id}] trace={trace_id}")

        # 同时发布到 Pub/Sub 频道（供 WebSocket 实时推送）
        await self.redis.publish(f"edict:pubsub:{topic}", json.dumps(event, ensure_ascii=False))

        return entry_id

    async def ensure_consumer_group(self, topic: str, group: str):
        """确保消费者组存在（幂等）。"""
        stream_key = self._stream_key(topic)
        try:
            await self.redis.xgroup_create(stream_key, group, id="0", mkstream=True)
            log.info(f"Created consumer group {group} on {stream_key}")
        except aioredis.ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise

    async def consume(
        self,
        topic: str,
        group: str,
        consumer: str,
        count: int = 10,
        block_ms: int = 5000,
    ) -> list[tuple[str, dict]]:
        """从消费者组消费事件。

        Returns:
            list of (entry_id, event_dict)
        """
        stream_key = self._stream_key(topic)
        results = await self.redis.xreadgroup(
            groupname=group,
            consumername=consumer,
            streams={stream_key: ">"},
            count=count,
            block=block_ms,
        )
        events = []
        if results:
            for _stream, messages in results:
                for entry_id, data in messages:
                    # 反序列化 JSON 字段
                    if "payload" in data:
                        data["payload"] = json.loads(data["payload"])
                    if "meta" in data:
                        data["meta"] = json.loads(data["meta"])
                    events.append((entry_id, data))
        return events

    async def ack(self, topic: str, group: str, entry_id: str):
        """确认消费 — ACK 后事件不会被重新投递。"""
        stream_key = self._stream_key(topic)
        await self.redis.xack(stream_key, group, entry_id)
        log.debug(f"✅ ACK {stream_key} [{entry_id}] group={group}")

    async def get_pending(self, topic: str, group: str, count: int = 10) -> list:
        """查看未 ACK 的 pending 事件（用于诊断和恢复）。"""
        stream_key = self._stream_key(topic)
        return await self.redis.xpending_range(stream_key, group, min="-", max="+", count=count)

    async def claim_stale(
        self,
        topic: str,
        group: str,
        consumer: str,
        min_idle_ms: int = 60000,
        count: int = 10,
    ) -> list[tuple[str, dict]]:
        """认领超时的 pending 事件（消费者崩溃恢复）。"""
        stream_key = self._stream_key(topic)
        results = await self.redis.xautoclaim(
            stream_key, group, consumer, min_idle_time=min_idle_ms, start_id="0-0", count=count
        )
        # xautoclaim returns (next_id, [(id, data), ...], [deleted_ids])
        if results and len(results) >= 2:
            events = []
            for entry_id, data in results[1]:
                if "payload" in data:
                    data["payload"] = json.loads(data["payload"])
                if "meta" in data:
                    data["meta"] = json.loads(data["meta"])
                events.append((entry_id, data))
            return events
        return []

    async def stream_info(self, topic: str) -> dict:
        """获取 Stream 信息（长度、消费者组等）。"""
        stream_key = self._stream_key(topic)
        try:
            info = await self.redis.xinfo_stream(stream_key)
            return info
        except aioredis.ResponseError:
            return {}


# ── 全局单例 ──
_bus: EventBus | None = None


async def get_event_bus() -> EventBus:
    global _bus
    if _bus is None:
        _bus = EventBus()
        await _bus.connect()
    return _bus
