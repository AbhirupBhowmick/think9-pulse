from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any


class PipelineRunBase(BaseModel):
    scenario_name: str
    user_query: Optional[str] = None
    status: str = "PENDING"
    source_type: str = "user"
    current_stage: str = "NOT_STARTED"
    error_message: Optional[str] = None


class PipelineRunCreate(PipelineRunBase):
    pass


class PipelineRunResponse(PipelineRunBase):
    id: UUID
    started_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PipelineTriggerResponse(BaseModel):
    message: str
    scenario_name: str
    status: str
    note: str
