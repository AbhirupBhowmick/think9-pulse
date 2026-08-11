"""
Pydantic Schemas for Think9 Pulse Multi-Agent Pipeline.
Defines input/output contracts for every specialized agent.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from uuid import UUID


# ==========================================
# 1. SIGNAL COLLECTOR SCHEMAS
# ==========================================

class NormalizedSignal(BaseModel):
    original_signal_id: str
    topic: str = Field(..., description="Concise main topic (max 8 words)")
    consumer_need: str = Field(..., description="Concise core consumer need (1 short sentence)")
    sentiment: float = Field(..., ge=-1.0, le=1.0, description="Sentiment score from -1.0 to 1.0")
    signal_strength: float = Field(..., ge=0.0, le=1.0, description="Signal strength score 0.0 to 1.0")
    category: str = Field(..., description="Product sector category")
    geographic_relevance: str = Field(default="US/Global", description="Target market geography")
    key_entities: List[str] = Field(default_factory=list, description="Extracted brand/product entities")
    rationale: Optional[str] = Field(default="Normalized from raw signal", description="Optional concise rationale")


class SignalCollectorOutput(BaseModel):
    signals: List[NormalizedSignal] = Field(..., description="List of normalized signal records")


# ==========================================
# 2. TREND DETECTION SCHEMAS
# ==========================================

class TrendAnalysis(BaseModel):
    trend_name: str = Field(..., description="Concise marketable trend name (max 6 words)")
    trend_description: str = Field(..., description="Concise trend description (1-2 short sentences)")
    sector: str = Field(..., description="Primary consumer sector")
    momentum_score: float = Field(..., ge=0.0, le=100.0, description="Momentum acceleration score (0-100)")
    confidence_score: float = Field(..., ge=0.0, le=100.0, description="Analytical confidence score (0-100)")
    growth_signal: str = Field(..., description="Key quantitative growth vector (e.g. '+145% YoY search spike')")
    supporting_signal_ids: List[str] = Field(..., description="List of supporting signal IDs")
    contradictory_signal_ids: List[str] = Field(default_factory=list, description="Optional signal IDs indicating headwind")
    rationale: Optional[str] = Field(default="Grounded in signal evidence consensus", description="Optional short rationale")
    trend_status: str = Field(default="EMERGING", description="EMERGING, PEAKING, MATURE, or DECLINING")


# ==========================================
# 3. CONSUMER INSIGHT SCHEMAS
# ==========================================

class ConsumerInsight(BaseModel):
    consumer_problem: str = Field(..., description="Primary core problem faced by target audience")
    consumer_need: str = Field(..., description="Explicit unfulfilled demand statement")
    target_consumer: str = Field(..., description="Target demographic and psychographic profile")
    jobs_to_be_done: str = Field(..., description="Jobs-To-Be-Done (JTBD) framework summary")
    motivations: List[str] = Field(..., description="Primary buying/usage drivers")
    pain_points: List[str] = Field(..., description="Frictions in current market offerings")
    barriers: List[str] = Field(..., description="Obstacles preventing consumer satisfaction")
    desired_outcome: str = Field(..., description="Ideal resolution state for the consumer")
    supporting_evidence: List[str] = Field(..., description="Direct evidence references from source signals")
    confidence_score: float = Field(..., ge=0.0, le=100.0, description="Insight validity confidence score")


# ==========================================
# 4. OPPORTUNITY GENERATOR SCHEMAS
# ==========================================

class ProductOpportunity(BaseModel):
    opportunity_title: str = Field(..., description="Catchy product title concept")
    product_concept: str = Field(..., description="High-level product concept overview")
    product_description: str = Field(..., description="Detailed feature set and format description")
    target_consumer: str = Field(..., description="Refined target consumer definition")
    consumer_need: str = Field(..., description="Specific consumer need addressed by concept")
    positioning: str = Field(..., description="Brand positioning statement vs competitors")
    differentiation: str = Field(..., description="Key unique selling propositions (USPs)")
    suggested_features: List[str] = Field(..., description="List of core product features and specs")
    recommended_next_action: str = Field(..., description="Actionable recommendation for R&D/Brand team")
    expected_value: str = Field(..., description="Estimated market opportunity size/tier")
    confidence_score: float = Field(..., ge=0.0, le=100.0, description="Opportunity feasibility score")


# ==========================================
# 5. BRAND MATCHER SCHEMAS
# ==========================================

class BrandMatchResult(BaseModel):
    recommended_brand_id: Optional[str] = Field(None, description="UUID of matched Think9 brand if matched")
    recommended_brand_name: str = Field(..., description="Name of best-fit Think9 portfolio brand")
    fit_score: float = Field(..., ge=0.0, le=100.0, description="Overall brand compatibility fit score (0-100)")
    strategic_fit: float = Field(..., ge=0.0, le=100.0, description="Alignment with brand strategic vision")
    category_fit: float = Field(..., ge=0.0, le=100.0, description="Category extension appropriateness")
    audience_fit: float = Field(..., ge=0.0, le=100.0, description="Target customer overlap")
    positioning_fit: float = Field(..., ge=0.0, le=100.0, description="Price & premium positioning fit")
    capability_fit: float = Field(..., ge=0.0, le=100.0, description="Estimated supply chain & R&D capability fit")
    alternative_brands: List[str] = Field(default_factory=list, description="Secondary alternative Think9 brand candidates")
    rationale: Optional[str] = Field(default="Brand fit matched to portfolio alignment", description="Optional analytical fit rationale")


# ==========================================
# 6. RISK / CONFIDENCE VALIDATOR SCHEMAS
# ==========================================

class RiskFactor(BaseModel):
    category: str = Field(..., description="Regulatory, Competitive, Supply Chain, Brand Cannibalization, Margin")
    severity: str = Field(..., description="Low, Medium, High, Critical")
    description: str = Field(..., description="Specific risk condition description")


class ValidationResult(BaseModel):
    overall_confidence: float = Field(..., ge=0.0, le=100.0, description="Final composite confidence score (0-100)")
    evidence_score: float = Field(..., ge=0.0, le=100.0, description="Evidence volume and diversity score")
    trend_reliability_score: float = Field(..., ge=0.0, le=100.0, description="Trend stability vs fad score")
    brand_fit_score: float = Field(..., ge=0.0, le=100.0, description="Validated brand match score")
    feasibility_score: float = Field(..., ge=0.0, le=100.0, description="Technical and commercial feasibility")
    risk_score: float = Field(..., ge=0.0, le=100.0, description="Composite risk index (lower is safer)")
    identified_risks: List[RiskFactor] = Field(default_factory=list, description="Audited business risks")
    missing_information: List[str] = Field(default_factory=list, description="Unaddressed gaps or required further data")
    validation_status: str = Field(..., description="APPROVED, NEEDS_REVIEW, or REJECTED")
    recommended_action: str = Field(..., description="Final executive decision recommendation")
    validation_summary: str = Field(..., description="Concise executive audit summary")


# ==========================================
# PIPELINE AUDIT & TRACE SCHEMAS
# ==========================================

class AgentExecutionStage(BaseModel):
    stage_name: str
    agent_name: str
    status: str  # SUCCESS, FAILED, DEMO_FALLBACK
    started_at: str
    completed_at: str
    execution_time_ms: int
    input_summary: str
    output_summary: str
    confidence_score: Optional[float] = None
    error: Optional[str] = None


class PipelineRunResult(BaseModel):
    pipeline_run_id: str
    scenario: str
    status: str
    opportunity_id: Optional[str] = None
    opportunity_title: Optional[str] = None
    matched_brand_name: Optional[str] = None
    validation_status: str
    confidence_score: float
    summary: str
    execution_stages: List[AgentExecutionStage] = Field(default_factory=list)
