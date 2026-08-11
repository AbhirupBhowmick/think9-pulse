from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.models.pipeline_run import PipelineRun
from app.schemas.pipeline import PipelineRunResponse
from agents.schemas import PipelineRunResult
from agents.orchestrator import PipelineOrchestrator

router = APIRouter()


@router.get("/pipeline/runs", response_model=List[PipelineRunResponse], summary="List Pipeline Execution Runs")
def list_pipeline_runs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    source_type: Optional[str] = Query(None, description="Filter by source_type ('user' or 'seed')"),
    db: Session = Depends(get_db)
):
    query = db.query(PipelineRun)
    if source_type:
        query = query.filter(PipelineRun.source_type == source_type)
    return query.order_by(PipelineRun.started_at.desc()).offset(skip).limit(limit).all()


@router.get("/pipeline/runs/{run_id}", response_model=PipelineRunResponse, summary="Get Pipeline Run by ID")
def get_pipeline_run(run_id: UUID, db: Session = Depends(get_db)):
    run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline run with ID {run_id} not found."
        )
    return run


@router.post("/pipeline/run", response_model=PipelineRunResult, status_code=status.HTTP_200_OK, summary="Trigger Agentic Pipeline Run")
def trigger_pipeline(
    scenario_name: str = Query("Consumer Query Analysis", description="Scenario identifier"),
    user_query: Optional[str] = Query(None, description="Custom consumer research question/query"),
    db: Session = Depends(get_db)
):
    """
    Trigger end-to-end multi-agent consumer intelligence pipeline.
    Executes all 6 autonomous agents sequentially and returns audit execution trace.
    """
    try:
        orchestrator = PipelineOrchestrator(db=db)
        result = orchestrator.run_pipeline(
            scenario_name=scenario_name,
            user_query=user_query
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline execution error: {str(e)}"
        )
