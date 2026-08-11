from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class BrandBase(BaseModel):
    name: str
    sector: str
    description: Optional[str] = None
    target_consumer: Optional[str] = None
    positioning: Optional[str] = None
    product_categories: List[str] = []


class BrandCreate(BrandBase):
    pass


class BrandResponse(BrandBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
