"""Event 模型 — 事件持久化表，支持回放和审计。

每个事件对应一次系统行为：任务创建、状态变更、Agent 思考、Todo 更新等。
遵循 Edict Architecture §3 事件结构规范。
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..db import Base


class Event(Base):
    """事件表 — 所有系统事件的持久化记录。"""
    __tablename__ = "events"

    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trace_id = Column(String(32), nullable=False, index=True, comment="关联任务ID")
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # 事件分类
    topic = Column(String(128), nullable=False, index=True, comment="事件主题, e.g. task.created")
    event_type = Column(String(128), nullable=False, comment="事件类型, e.g. state.changed")
    producer = Column(String(128), nullable=False, comment="事件生产者, e.g. orchestrator:v1")

    # 事件数据
    payload = Column(JSONB, default=dict, comment="事件负载")
    meta = Column(JSONB, default=dict, comment="元数据 {priority, model, version}")

    __table_args__ = (
        Index("ix_events_trace_topic", "trace_id", "topic"),
        Index("ix_events_timestamp", "timestamp"),
    )

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "trace_id": self.trace_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else "",
            "topic": self.topic,
            "event_type": self.event_type,
            "producer": self.producer,
            "payload": self.payload or {},
            "meta": self.meta or {},
        }
