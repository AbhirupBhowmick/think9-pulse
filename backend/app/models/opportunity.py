import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trend_id = Column(UUID(as_uuid=True), ForeignKey("trends.id", ondelete="SET NULL"), nullable=True, index=True)
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    consumer_need = Column(Text, nullable=False)
    target_consumer = Column(Text, nullable=False)
    product_concept = Column(Text, nullable=False)
    positioning = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=False, default=0.0)
    risk_score = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="IN_REVIEW", index=True)
    source_type = Column(String(20), nullable=False, default="user", index=True)
    recommended_action = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    trend = relationship("Trend", back_populates="opportunities")
    brand = relationship("Brand", back_populates="opportunities")
