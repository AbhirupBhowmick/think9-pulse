import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False, unique=True, index=True)
    sector = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    target_consumer = Column(Text, nullable=True)
    positioning = Column(Text, nullable=True)
    product_categories = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    opportunities = relationship("Opportunity", back_populates="brand")
