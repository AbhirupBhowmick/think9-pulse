from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class TrendBase(BaseModel):
    name: str
    description: str
    sector: str
    momentum_score: float = 0.0
    confidence_score: float = 0.0
    growth_rate: float = 0.0
    signal_count: int = 0
    status: str = "EMERGING"


class TrendCreate(TrendBase):
    pass


class TrendResponse(TrendBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
