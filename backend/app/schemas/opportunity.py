from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.schemas.brand import BrandResponse
from app.schemas.trend import TrendResponse
from app.schemas.signal import SignalResponse


class EvidenceResponse(BaseModel):
    id: UUID
    trend_id: UUID
    signal_id: UUID
    evidence_type: str
    relevance_score: float
    explanation: str
    created_at: datetime
    signal: Optional[SignalResponse] = None

    model_config = ConfigDict(from_attributes=True)


class OpportunityBase(BaseModel):
    title: str
    description: str
    consumer_need: str
    target_consumer: str
    product_concept: str
    positioning: str
    confidence_score: float = 0.0
    risk_score: float = 0.0
    status: str = "IN_REVIEW"
    source_type: str = "user"
    recommended_action: Optional[str] = None


class OpportunityCreate(OpportunityBase):
    trend_id: Optional[UUID] = None
    brand_id: Optional[UUID] = None


class OpportunityResponse(OpportunityBase):
    id: UUID
    trend_id: Optional[UUID] = None
    brand_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    brand: Optional[BrandResponse] = None

    model_config = ConfigDict(from_attributes=True)


class OpportunityDetailResponse(OpportunityResponse):
    trend: Optional[TrendResponse] = None
    evidence: List[EvidenceResponse] = []

    model_config = ConfigDict(from_attributes=True)
