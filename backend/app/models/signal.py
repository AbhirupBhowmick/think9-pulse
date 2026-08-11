import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

try:
    from pgvector.sqlalchemy import Vector
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False


class Signal(Base):
    __tablename__ = "signals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String(100), nullable=False, index=True)
    source_url = Column(Text, nullable=True)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    signal_type = Column(String(100), nullable=False, index=True)
    sector = Column(String(100), nullable=False, index=True)
    sentiment = Column(Float, nullable=False, default=0.0)
    signal_strength = Column(Float, nullable=False, default=0.5)
    geography = Column(String(100), default="US/Global")
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    metadata_ = Column("metadata", JSON, default=dict)
    
    if HAS_PGVECTOR:
        embedding = Column(Vector(768), nullable=True)
    else:
        embedding = Column(JSON, nullable=True)

    evidences = relationship("Evidence", back_populates="signal", cascade="all, delete-orphan")
