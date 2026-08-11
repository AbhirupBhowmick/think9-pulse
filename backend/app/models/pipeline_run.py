import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_name = Column(String(150), nullable=False)
    user_query = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="PENDING", index=True)
    source_type = Column(String(20), nullable=False, default="user", index=True)
    current_stage = Column(String(100), nullable=False, default="NOT_STARTED")
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
