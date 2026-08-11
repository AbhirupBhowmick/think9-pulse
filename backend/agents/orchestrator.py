"""
Agent Orchestrator for Think9 Pulse.
Executes multi-step agentic consumer intelligence pipeline and records audit traces.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from agents.schemas import (
    SignalCollectorOutput, TrendAnalysis, ConsumerInsight,
    ProductOpportunity, BrandMatchResult, ValidationResult,
    AgentExecutionStage, PipelineRunResult
)
from agents.signal_collector import SignalCollectorAgent
from agents.trend_detection import TrendDetectionAgent
from agents.consumer_insight import ConsumerInsightAgent
from agents.opportunity_generator import OpportunityGeneratorAgent
from agents.brand_matcher import BrandMatcherAgent
from agents.risk_validator import RiskValidatorAgent

from app.models.brand import Brand
from app.models.signal import Signal
from app.models.trend import Trend
from app.models.evidence import Evidence
from app.models.opportunity import Opportunity
from app.models.pipeline_run import PipelineRun

logger = logging.getLogger("think9-pulse.orchestrator")


class PipelineOrchestrator:
    def __init__(self, db: Optional[Session] = None, demo_mode: bool = False):
        self.db = db
        self.signal_collector = SignalCollectorAgent(demo_mode=demo_mode)
        self.trend_detector = TrendDetectionAgent(demo_mode=demo_mode)
        self.consumer_insight = ConsumerInsightAgent(demo_mode=demo_mode)
        self.opportunity_generator = OpportunityGeneratorAgent(demo_mode=demo_mode)
        self.brand_matcher = BrandMatcherAgent(demo_mode=demo_mode)
        self.risk_validator = RiskValidatorAgent(demo_mode=demo_mode)

    def run_pipeline(
        self,
        scenario_name: str = "Consumer Query Analysis",
        user_query: Optional[str] = None,
        input_signals: Optional[List[Dict[str, Any]]] = None,
        input_brands: Optional[List[Dict[str, Any]]] = None
    ) -> PipelineRunResult:
        run_id = str(uuid.uuid4())
        logger.info(f"[PIPELINE] Started pipeline run {run_id} for scenario '{scenario_name}'")
        
        stages_trace: List[AgentExecutionStage] = []

        # 0. Load Data if DB session is available and inputs are not provided
        if self.db:
            if not input_signals:
                db_signals = self.db.query(Signal).limit(4).all()
                input_signals = [
                    {
                        "id": str(s.id),
                        "source": s.source,
                        "title": s.title,
                        "content": s.content,
                        "sector": s.sector,
                        "sentiment": s.sentiment,
                        "signal_strength": s.signal_strength,
                        "geography": s.geography
                    }
                    for s in db_signals
                ]
            if not input_brands:
                db_brands = self.db.query(Brand).all()
                input_brands = [
                    {
                        "id": str(b.id),
                        "name": b.name,
                        "sector": b.sector,
                        "description": b.description,
                        "target_consumer": b.target_consumer,
                        "positioning": b.positioning,
                        "product_categories": b.product_categories
                    }
                    for b in db_brands
                ]

        input_signals = input_signals or []
        input_brands = input_brands or []

        # Track PipelineRun in DB
        db_pipeline_run = None
        if self.db:
            db_pipeline_run = PipelineRun(
                id=uuid.UUID(run_id),
                scenario_name=user_query[:100] if user_query else scenario_name,
                user_query=user_query,
                status="RUNNING",
                source_type="user",
                current_stage="SIGNAL_COLLECTION",
                started_at=datetime.now(timezone.utc)
            )
            self.db.add(db_pipeline_run)
            self.db.commit()

        try:
            # Stage 1: Signal Collector Agent
            logger.info("[AGENT] Signal Collector Agent starting...")
            norm_output, sc_meta = self.signal_collector.process_signals(input_signals, user_query=user_query)
            # Stage 1: Signal Collector Agent
            logger.info("[AGENT] Signal Collector Agent starting...")
            norm_output, sc_meta = self.signal_collector.process_signals(input_signals, user_query=user_query)
            stages_trace.append(
                AgentExecutionStage(
                    stage_name="1. Understand the Consumer",
                    agent_name="SignalCollectorAgent",
                    status=sc_meta["status"],
                    started_at=sc_meta["started_at"],
                    completed_at=sc_meta["completed_at"],
                    execution_time_ms=sc_meta["execution_time_ms"],
                    input_summary=f"Ingested {len(input_signals)} raw multi-channel consumer signals.",
                    output_summary=f"Normalized {len(norm_output.signals)} signals with sentiment and entity tags."
                )
            )

            # Stage 2: Trend Detection Agent
            if db_pipeline_run and self.db:
                db_pipeline_run.current_stage = "TREND_DETECTION"
                self.db.commit()

            logger.info("[AGENT] Trend Detection Agent starting...")
            trend_output, td_meta = self.trend_detector.analyze_trend(norm_output, user_query=user_query)
            stages_trace.append(
                AgentExecutionStage(
                    stage_name="2. Find Emerging Trends",
                    agent_name="TrendDetectionAgent",
                    status=td_meta["status"],
                    started_at=td_meta["started_at"],
                    completed_at=td_meta["completed_at"],
                    execution_time_ms=td_meta["execution_time_ms"],
                    input_summary=f"Analyzed {len(norm_output.signals)} normalized signals.",
                    output_summary=f"Detected trend candidate '{trend_output.trend_name}' with momentum {trend_output.momentum_score}/100.",
                    confidence_score=trend_output.confidence_score
                )
            )

            # Stage 3: Consumer Insight Agent
            if db_pipeline_run and self.db:
                db_pipeline_run.current_stage = "CONSUMER_INSIGHT"
                self.db.commit()

            logger.info("[AGENT] Consumer Insight Agent starting...")
            insight_output, ci_meta = self.consumer_insight.generate_insight(trend_output, norm_output, user_query=user_query)
            stages_trace.append(
                AgentExecutionStage(
                    stage_name="3. Understand What People Need",
                    agent_name="ConsumerInsightAgent",
                    status=ci_meta["status"],
                    started_at=ci_meta["started_at"],
                    completed_at=ci_meta["completed_at"],
                    execution_time_ms=ci_meta["execution_time_ms"],
                    input_summary=f"Synthesized insight from trend '{trend_output.trend_name}'.",
                    output_summary=f"Formulated JTBD framework and identified core consumer pain points.",
                    confidence_score=insight_output.confidence_score
                )
            )

            # Stage 4: Opportunity Generator Agent
            if db_pipeline_run and self.db:
                db_pipeline_run.current_stage = "OPPORTUNITY_GENERATION"
                self.db.commit()

            logger.info("[AGENT] Opportunity Generator Agent starting...")
            opp_output, og_meta = self.opportunity_generator.generate_opportunity(insight_output, trend_output, user_query=user_query)
            stages_trace.append(
                AgentExecutionStage(
                    stage_name="4. Suggest a Product Opportunity",
                    agent_name="OpportunityGeneratorAgent",
                    status=og_meta["status"],
                    started_at=og_meta["started_at"],
                    completed_at=og_meta["completed_at"],
                    execution_time_ms=og_meta["execution_time_ms"],
                    input_summary=f"Translated consumer insight into commercial product proposal.",
                    output_summary=f"Generated product concept '{opp_output.opportunity_title}'.",
                    confidence_score=opp_output.confidence_score
                )
            )

            # Stage 5: Brand Matcher Agent
            if db_pipeline_run and self.db:
                db_pipeline_run.current_stage = "BRAND_MATCHING"
                self.db.commit()

            logger.info("[AGENT] Brand Matcher Agent starting...")
            brand_output, bm_meta = self.brand_matcher.match_brand(opp_output, input_brands)
            stages_trace.append(
                AgentExecutionStage(
                    stage_name="5. Find the Best Brand Fit",
                    agent_name="BrandMatcherAgent",
                    status=bm_meta["status"],
                    started_at=bm_meta["started_at"],
                    completed_at=bm_meta["completed_at"],
                    execution_time_ms=bm_meta["execution_time_ms"],
                    input_summary=f"Compared opportunity against {len(input_brands)} Think9 portfolio brands.",
                    output_summary=f"Matched opportunity to brand '{brand_output.recommended_brand_name}' with fit score {brand_output.fit_score}/100.",
                    confidence_score=brand_output.fit_score
                )
            )

            # Stage 6: Risk / Confidence Validation Agent
            if db_pipeline_run and self.db:
                db_pipeline_run.current_stage = "RISK_VALIDATION"
                self.db.commit()

            logger.info("[AGENT] Risk Validator Agent starting...")
            val_output, rv_meta = self.risk_validator.validate_opportunity(
                trend_output, insight_output, opp_output, brand_output
            )
            stages_trace.append(
                AgentExecutionStage(
                    stage_name="6. Check Confidence & Risks",
                    agent_name="RiskValidatorAgent",
                    status=rv_meta["status"],
                    started_at=rv_meta["started_at"],
                    completed_at=rv_meta["completed_at"],
                    execution_time_ms=rv_meta["execution_time_ms"],
                    input_summary=f"Audited opportunity evidence, brand fit, and commercial risks.",
                    output_summary=f"Validation status '{val_output.validation_status}' with overall confidence {val_output.overall_confidence}%.",
                    confidence_score=val_output.overall_confidence
                )
            )

            # 7. Persist to Database if session exists
            created_opp_id = None
            if self.db:
                # Find matched brand UUID
                matched_brand_uuid = None
                if brand_output.recommended_brand_id:
                    try:
                        matched_brand_uuid = uuid.UUID(brand_output.recommended_brand_id)
                    except ValueError:
                        pass
                
                if not matched_brand_uuid:
                    b_obj = self.db.query(Brand).filter(Brand.name == brand_output.recommended_brand_name).first()
                    if b_obj:
                        matched_brand_uuid = b_obj.id

                # Update or create Trend record
                existing_trend = self.db.query(Trend).filter(Trend.name == trend_output.trend_name).first()
                if not existing_trend:
                    existing_trend = Trend(
                        id=uuid.uuid4(),
                        name=trend_output.trend_name,
                        description=trend_output.trend_description,
                        sector=trend_output.sector,
                        momentum_score=trend_output.momentum_score,
                        confidence_score=trend_output.confidence_score,
                        growth_rate=145.0,
                        signal_count=len(norm_output.signals),
                        status=trend_output.trend_status
                    )
                    self.db.add(existing_trend)
                    self.db.commit()

                # Create Opportunity Record
                opp_id = uuid.uuid4()
                created_opp_id = str(opp_id)
                db_opportunity = Opportunity(
                    id=opp_id,
                    trend_id=existing_trend.id,
                    brand_id=matched_brand_uuid,
                    title=opp_output.opportunity_title,
                    description=opp_output.product_concept,
                    consumer_need=opp_output.consumer_need,
                    target_consumer=opp_output.target_consumer,
                    product_concept=opp_output.product_description,
                    positioning=opp_output.positioning,
                    confidence_score=val_output.overall_confidence,
                    risk_score=val_output.risk_score,
                    status=val_output.validation_status,
                    source_type="user",
                    recommended_action=val_output.recommended_action
                )
                self.db.add(db_opportunity)

                # Update PipelineRun status
                if db_pipeline_run:
                    db_pipeline_run.status = "COMPLETED"
                    db_pipeline_run.current_stage = "COMPLETED"
                    db_pipeline_run.completed_at = datetime.now(timezone.utc)

                self.db.commit()

            logger.info(f"[PIPELINE] Pipeline run {run_id} completed successfully.")

            return PipelineRunResult(
                pipeline_run_id=run_id,
                scenario=scenario_name,
                status="completed",
                opportunity_id=created_opp_id,
                opportunity_title=opp_output.opportunity_title,
                matched_brand_name=brand_output.recommended_brand_name,
                validation_status=val_output.validation_status,
                confidence_score=val_output.overall_confidence,
                summary=val_output.validation_summary,
                execution_stages=stages_trace
            )

        except Exception as e:
            logger.error(f"[PIPELINE] Pipeline run failed: {e}", exc_info=True)
            if db_pipeline_run and self.db:
                db_pipeline_run.status = "FAILED"
                db_pipeline_run.error_message = str(e)
                self.db.commit()
            
            raise e
