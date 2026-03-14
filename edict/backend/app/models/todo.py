"""Todo 模型 — 结构化子任务。

遵循 Edict Architecture §4 Todo JSON Schema。
支持层级结构（parent_id）和 checkpoint 跟踪。
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..db import Base


class Todo(Base):
    """结构化子任务表。"""
    __tablename__ = "todos"

    todo_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trace_id = Column(String(32), nullable=False, index=True, comment="关联任务ID")
    parent_id = Column(UUID(as_uuid=True), nullable=True, comment="父级 todo_id（树状结构）")

    title = Column(String(256), nullable=False, comment="子任务标题")
    description = Column(Text, default="", comment="详细描述")
    owner = Column(String(64), default="", comment="负责部门")
    assignee_agent = Column(String(32), default="", comment="执行 Agent")

    status = Column(String(32), nullable=False, default="open", index=True,
                    comment="状态: open|in_progress|done|cancelled")
    priority = Column(String(16), default="normal", comment="优先级: low|normal|high|urgent")
    estimated_cost = Column(Float, default=0.0, comment="预估 token 耗费")

    created_by = Column(String(64), default="", comment="创建者")
    checkpoints = Column(JSONB, default=list, comment="检查点 [{name, status}]")
    metadata_ = Column("metadata", JSONB, default=dict, comment="扩展元数据")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_todos_trace_status", "trace_id", "status"),
    )

    def to_dict(self) -> dict:
        return {
            "todo_id": str(self.todo_id),
            "trace_id": self.trace_id,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "title": self.title,
            "description": self.description,
            "owner": self.owner,
            "assignee_agent": self.assignee_agent,
            "status": self.status,
            "priority": self.priority,
            "estimated_cost": self.estimated_cost,
            "created_by": self.created_by,
            "checkpoints": self.checkpoints or [],
            "metadata": self.metadata_ or {},
            "created_at": self.created_at.isoformat() if self.created_at else "",
            "updated_at": self.updated_at.isoformat() if self.updated_at else "",
        }
