"""Thought 模型 — Agent 思考流持久化。

遵循 Edict Architecture §4 Thought JSON Schema。
支持 streaming partial thoughts 和 dashboard 实时展示。
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID

from ..db import Base


class Thought(Base):
    """Agent 思考记录。"""
    __tablename__ = "thoughts"

    thought_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trace_id = Column(String(32), nullable=False, index=True, comment="关联任务ID")
    agent = Column(String(32), nullable=False, index=True, comment="Agent 标识")
    step = Column(Integer, nullable=False, default=0, comment="思考步骤序号")
    type = Column(
        String(32),
        nullable=False,
        default="reasoning",
        comment="思考类型: reasoning|query|action_intent|summary",
    )
    source = Column(String(16), default="llm", comment="来源: llm|tool|human")
    content = Column(Text, nullable=False, default="", comment="思考内容")
    tokens = Column(Integer, default=0, comment="消耗 token 数")
    confidence = Column(Float, default=0.0, comment="置信度 0-1")
    sensitive = Column(Boolean, default=False, comment="是否敏感内容")
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        Index("ix_thoughts_trace_agent", "trace_id", "agent"),
        Index("ix_thoughts_timestamp", "timestamp"),
    )

    def to_dict(self) -> dict:
        return {
            "thought_id": str(self.thought_id),
            "trace_id": self.trace_id,
            "agent": self.agent,
            "step": self.step,
            "type": self.type,
            "source": self.source,
            "content": self.content,
            "tokens": self.tokens,
            "confidence": self.confidence,
            "sensitive": self.sensitive,
            "timestamp": self.timestamp.isoformat() if self.timestamp else "",
        }
