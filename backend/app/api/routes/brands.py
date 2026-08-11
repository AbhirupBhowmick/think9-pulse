from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.models.brand import Brand
from app.schemas.brand import BrandResponse

router = APIRouter()


@router.get("/brands", response_model=List[BrandResponse], summary="List Think9 Portfolio Brands")
def list_brands(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    db: Session = Depends(get_db)
):
    query = db.query(Brand)
    if sector:
        query = query.filter(Brand.sector == sector)
    return query.offset(skip).limit(limit).all()


@router.get("/brands/{brand_id}", response_model=BrandResponse, summary="Get Brand by ID")
def get_brand(brand_id: UUID, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand with ID {brand_id} not found."
        )
    return brand
