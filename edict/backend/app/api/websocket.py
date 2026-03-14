"""WebSocket 端点 — 实时推送事件到前端。

取代旧架构的 5 秒 HTTP 轮询，改为：
- 客户端 WebSocket 连接
- 服务端订阅 Redis Pub/Sub 频道
- 实时推送事件（状态变更、Agent 思考流、心跳等）
"""

import asyncio
import json
import logging

import redis.asyncio as aioredis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..config import get_settings
from ..services.event_bus import get_event_bus

log = logging.getLogger("edict.ws")
router = APIRouter()

# 活跃连接管理
_connections: set[WebSocket] = set()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """主 WebSocket 端点 — 推送所有事件。"""
    await ws.accept()
    _connections.add(ws)
    log.info(f"WebSocket connected. Total: {len(_connections)}")

    # 创建独立的 Redis Pub/Sub 连接
    settings = get_settings()
    pubsub_redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    pubsub = pubsub_redis.pubsub()

    # 订阅所有 edict 频道
    await pubsub.psubscribe("edict:pubsub:*")

    try:
        # 并发：监听 Redis Pub/Sub + 客户端消息
        await asyncio.gather(
            _relay_events(pubsub, ws),
            _handle_client_messages(ws),
        )
    except WebSocketDisconnect:
        log.info("WebSocket disconnected")
    except Exception as e:
        log.error(f"WebSocket error: {e}")
    finally:
        _connections.discard(ws)
        await pubsub.punsubscribe("edict:pubsub:*")
        await pubsub_redis.aclose()
        log.info(f"WebSocket cleaned up. Remaining: {len(_connections)}")


async def _relay_events(pubsub, ws: WebSocket):
    """从 Redis Pub/Sub 接收事件，推送到 WebSocket。"""
    async for message in pubsub.listen():
        if message["type"] == "pmessage":
            channel = message["channel"]
            data = message["data"]

            # 提取 topic 名
            topic = channel.replace("edict:pubsub:", "") if channel.startswith("edict:pubsub:") else channel

            try:
                event_data = json.loads(data) if isinstance(data, str) else data
                await ws.send_json({
                    "type": "event",
                    "topic": topic,
                    "data": event_data,
                })
            except Exception as e:
                log.warning(f"Failed to relay event: {e}")
                break


async def _handle_client_messages(ws: WebSocket):
    """处理客户端发送的消息（心跳、订阅过滤等）。"""
    while True:
        try:
            data = await ws.receive_json()
            msg_type = data.get("type", "")

            if msg_type == "ping":
                await ws.send_json({"type": "pong"})
            elif msg_type == "subscribe":
                # 前端可请求只订阅特定 topic（未来扩展）
                topics = data.get("topics", [])
                log.debug(f"Client subscribe request: {topics}")
                await ws.send_json({"type": "subscribed", "topics": topics})
            else:
                log.debug(f"Unknown client message: {msg_type}")

        except WebSocketDisconnect:
            raise
        except Exception:
            break


@router.websocket("/ws/task/{task_id}")
async def task_websocket(ws: WebSocket, task_id: str):
    """单任务 WebSocket — 只推送与特定任务相关的事件。"""
    await ws.accept()
    _connections.add(ws)

    settings = get_settings()
    pubsub_redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    pubsub = pubsub_redis.pubsub()
    await pubsub.psubscribe("edict:pubsub:*")

    try:
        async for message in pubsub.listen():
            if message["type"] == "pmessage":
                data = message["data"]
                try:
                    event_data = json.loads(data) if isinstance(data, str) else data
                    payload = event_data.get("payload", {})
                    if isinstance(payload, str):
                        payload = json.loads(payload)

                    # 只转发与此任务相关的事件
                    if payload.get("task_id") == task_id:
                        topic = message["channel"].replace("edict:pubsub:", "")
                        await ws.send_json({
                            "type": "event",
                            "topic": topic,
                            "data": event_data,
                        })
                except Exception:
                    continue
    except WebSocketDisconnect:
        pass
    finally:
        _connections.discard(ws)
        await pubsub.punsubscribe("edict:pubsub:*")
        await pubsub_redis.aclose()


async def broadcast(event: dict):
    """向所有连接的 WebSocket 客户端广播事件（服务端内部调用用）。"""
    dead = set()
    for ws in _connections:
        try:
            await ws.send_json(event)
        except Exception:
            dead.add(ws)
    _connections -= dead
