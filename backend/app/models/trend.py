import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Trend(Base):
    __tablename__ = "trends"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    sector = Column(String(100), nullable=False, index=True)
    momentum_score = Column(Float, nullable=False, default=0.0)
    confidence_score = Column(Float, nullable=False, default=0.0)
    growth_rate = Column(Float, nullable=False, default=0.0)
    signal_count = Column(Integer, nullable=False, default=0)
    status = Column(String(50), nullable=False, default="EMERGING", index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    evidences = relationship("Evidence", back_populates="trend", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="trend")
