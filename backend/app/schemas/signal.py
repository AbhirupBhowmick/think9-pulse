from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any


class SignalBase(BaseModel):
    source: str
    source_url: Optional[str] = None
    title: Optional[str] = None
    content: str
    signal_type: str
    sector: str
    sentiment: float = 0.0
    signal_strength: float = 0.5
    geography: str = "US/Global"
    metadata_: Dict[str, Any] = Field(default_factory=dict, alias="metadata")


class SignalCreate(SignalBase):
    pass


class SignalResponse(BaseModel):
    id: UUID
    source: str
    source_url: Optional[str] = None
    title: Optional[str] = None
    content: str
    signal_type: str
    sector: str
    sentiment: float
    signal_strength: float
    geography: str
    detected_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict, validation_alias="metadata_")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
