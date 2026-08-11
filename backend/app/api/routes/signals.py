from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.models.signal import Signal
from app.schemas.signal import SignalResponse

router = APIRouter()


@router.get("/signals", response_model=List[SignalResponse], summary="List Ingested Consumer Signals")
def list_signals(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    source: Optional[str] = Query(None, description="Filter by signal source"),
    db: Session = Depends(get_db)
):
    query = db.query(Signal)
    if sector:
        query = query.filter(Signal.sector == sector)
    if source:
        query = query.filter(Signal.source == source)
    return query.order_by(Signal.detected_at.desc()).offset(skip).limit(limit).all()


@router.get("/signals/{signal_id}", response_model=SignalResponse, summary="Get Signal by ID")
def get_signal(signal_id: UUID, db: Session = Depends(get_db)):
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not signal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Signal with ID {signal_id} not found."
        )
    return signal
