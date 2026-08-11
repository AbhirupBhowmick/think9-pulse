from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.models.opportunity import Opportunity
from app.models.evidence import Evidence
from app.schemas.opportunity import OpportunityResponse, OpportunityDetailResponse, EvidenceResponse

router = APIRouter()


@router.get("/opportunities", response_model=List[OpportunityResponse], summary="List Product Opportunities")
def list_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    brand_id: Optional[UUID] = Query(None, description="Filter by matched Think9 brand"),
    source_type: Optional[str] = Query(None, description="Filter by source_type ('user' or 'seed')"),
    db: Session = Depends(get_db)
):
    query = db.query(Opportunity).options(joinedload(Opportunity.brand))
    if status_filter:
        query = query.filter(Opportunity.status == status_filter)
    if brand_id:
        query = query.filter(Opportunity.brand_id == brand_id)
    if source_type:
        query = query.filter(Opportunity.source_type == source_type)
    return query.order_by(Opportunity.confidence_score.desc()).offset(skip).limit(limit).all()


@router.get("/opportunities/{opportunity_id}", response_model=OpportunityDetailResponse, summary="Get Opportunity Details & Evidence")
def get_opportunity(opportunity_id: UUID, db: Session = Depends(get_db)):
    opp = db.query(Opportunity).options(
        joinedload(Opportunity.brand),
        joinedload(Opportunity.trend)
    ).filter(Opportunity.id == opportunity_id).first()

    if not opp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity with ID {opportunity_id} not found."
        )

    # Fetch associated evidence for the opportunity's trend
    evidences = []
    if opp.trend_id:
        evidences = db.query(Evidence).options(
            joinedload(Evidence.signal)
        ).filter(Evidence.trend_id == opp.trend_id).all()

    return OpportunityDetailResponse(
        id=opp.id,
        trend_id=opp.trend_id,
        brand_id=opp.brand_id,
        title=opp.title,
        description=opp.description,
        consumer_need=opp.consumer_need,
        target_consumer=opp.target_consumer,
        product_concept=opp.product_concept,
        positioning=opp.positioning,
        confidence_score=opp.confidence_score,
        risk_score=opp.risk_score,
        status=opp.status,
        recommended_action=opp.recommended_action,
        created_at=opp.created_at,
        updated_at=opp.updated_at,
        brand=opp.brand,
        trend=opp.trend,
        evidence=evidences
    )


@router.get("/opportunities/{opportunity_id}/evidence", response_model=List[EvidenceResponse], summary="Get Evidence Signals for Opportunity")
def get_opportunity_evidence(opportunity_id: UUID, db: Session = Depends(get_db)):
    opp = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity with ID {opportunity_id} not found."
        )

    if not opp.trend_id:
        return []

    evidences = db.query(Evidence).options(
        joinedload(Evidence.signal)
    ).filter(Evidence.trend_id == opp.trend_id).all()

    return evidences
