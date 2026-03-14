"""Events API — 事件查询与审计。"""

import logging
from datetime import datetime

from fastapi import APIRouter, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from ..db import get_db
from ..models.event import Event
from ..services.event_bus import get_event_bus

log = logging.getLogger("edict.api.events")
router = APIRouter()


@router.get("")
async def list_events(
    trace_id: str | None = None,
    topic: str | None = None,
    producer: str | None = None,
    limit: int = Query(default=50, le=500),
    db: AsyncSession = Depends(get_db),
):
    """查询持久化事件（从 Postgres event 表）。"""
    stmt = select(Event)
    if trace_id:
        stmt = stmt.where(Event.trace_id == trace_id)
    if topic:
        stmt = stmt.where(Event.topic == topic)
    if producer:
        stmt = stmt.where(Event.producer == producer)
    stmt = stmt.order_by(Event.timestamp.desc()).limit(limit)
    result = await db.execute(stmt)
    events = result.scalars().all()
    return {
        "events": [
            {
                "event_id": str(e.event_id),
                "trace_id": e.trace_id,
                "topic": e.topic,
                "event_type": e.event_type,
                "producer": e.producer,
                "payload": e.payload,
                "meta": e.meta,
                "timestamp": e.timestamp.isoformat() if e.timestamp else None,
            }
            for e in events
        ],
        "count": len(events),
    }


@router.get("/stream-info")
async def stream_info(topic: str = Query(description="Stream topic")):
    """查询 Redis Stream 实时信息。"""
    bus = await get_event_bus()
    info = await bus.stream_info(topic)
    return {"topic": topic, "info": info}


@router.get("/topics")
async def list_topics():
    """列出所有可用事件 topic。"""
    from ..services.event_bus import (
        TOPIC_TASK_CREATED,
        TOPIC_TASK_STATUS,
        TOPIC_TASK_DISPATCH,
        TOPIC_TASK_COMPLETED,
        TOPIC_TASK_STALLED,
        TOPIC_AGENT_THOUGHTS,
        TOPIC_AGENT_HEARTBEAT,
    )
    return {
        "topics": [
            {"name": TOPIC_TASK_CREATED, "description": "任务创建"},
            {"name": TOPIC_TASK_STATUS, "description": "状态变更"},
            {"name": TOPIC_TASK_DISPATCH, "description": "Agent 派发"},
            {"name": TOPIC_TASK_COMPLETED, "description": "任务完成"},
            {"name": TOPIC_TASK_STALLED, "description": "任务停滞"},
            {"name": TOPIC_AGENT_THOUGHTS, "description": "Agent 思考流"},
            {"name": TOPIC_AGENT_HEARTBEAT, "description": "Agent 心跳"},
        ]
    }
