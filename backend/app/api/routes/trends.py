from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.models.trend import Trend
from app.schemas.trend import TrendResponse

router = APIRouter()


@router.get("/trends", response_model=List[TrendResponse], summary="List Detected Trends")
def list_trends(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (EMERGING, PEAKING, etc.)"),
    db: Session = Depends(get_db)
):
    query = db.query(Trend)
    if sector:
        query = query.filter(Trend.sector == sector)
    if status_filter:
        query = query.filter(Trend.status == status_filter)
    return query.order_by(Trend.momentum_score.desc()).offset(skip).limit(limit).all()


@router.get("/trends/{trend_id}", response_model=TrendResponse, summary="Get Trend by ID")
def get_trend(trend_id: UUID, db: Session = Depends(get_db)):
    trend = db.query(Trend).filter(Trend.id == trend_id).first()
    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trend with ID {trend_id} not found."
        )
    return trend
