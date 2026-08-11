"""
Unit & Integration Tests for Think9 Pulse Agent Suite.
Validates Pydantic schemas, BaseAgent, 6 specialized agents, orchestrator, and pipeline API endpoint.
Mocks external Gemini API calls to ensure test suite does not consume live API credits.
"""

import os
os.environ["DEMO_MODE"] = "true"

import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from agents.schemas import (
    NormalizedSignal, SignalCollectorOutput,
    TrendAnalysis, ConsumerInsight, ProductOpportunity,
    BrandMatchResult, ValidationResult, RiskFactor,
    PipelineRunResult
)
from agents.base_agent import BaseAgent
from agents.signal_collector import SignalCollectorAgent
from agents.trend_detection import TrendDetectionAgent
from agents.consumer_insight import ConsumerInsightAgent
from agents.opportunity_generator import OpportunityGeneratorAgent
from agents.brand_matcher import BrandMatcherAgent
from agents.risk_validator import RiskValidatorAgent
from agents.orchestrator import PipelineOrchestrator


# ==========================================
# 1. TEST SCHEMAS
# ==========================================

def test_pydantic_schemas_validation():
    sig = NormalizedSignal(
        original_signal_id="123",
        topic="Savory Protein",
        consumer_need="High protein quick savory morning meal",
        sentiment=0.8,
        signal_strength=0.9,
        category="Food & Beverage",
        geographic_relevance="US",
        key_entities=["Egg Bites"],
        rationale="Clear savory preference"
    )
    assert sig.sentiment == 0.8
    assert sig.signal_strength == 0.9

    output = SignalCollectorOutput(signals=[sig])
    assert len(output.signals) == 1

    val = ValidationResult(
        overall_confidence=91.0,
        evidence_score=90.0,
        trend_reliability_score=92.0,
        brand_fit_score=95.0,
        feasibility_score=88.0,
        risk_score=15.0,
        identified_risks=[
            RiskFactor(category="Supply Chain", severity="Medium", description="Cold chain requirement")
        ],
        missing_information=[],
        validation_status="APPROVED",
        recommended_action="Proceed to pilot",
        validation_summary="High confidence opportunity"
    )
    assert val.validation_status == "APPROVED"
    assert val.overall_confidence == 91.0


# ==========================================
# 2. TEST BASE AGENT CONFIG
# ==========================================

def test_base_agent_initialization():
    agent = BaseAgent(
        agent_name="TestAgent",
        system_instruction="Test instruction",
        temperature=0.3,
        demo_mode=True
    )
    assert agent.agent_name == "TestAgent"
    assert agent.temperature == 0.3
    assert agent.demo_mode is True


# ==========================================
# 3. TEST AGENT 1: SIGNAL COLLECTOR (MOCKED)
# ==========================================

def test_signal_collector_agent():
    agent = SignalCollectorAgent(demo_mode=True)
    raw_signals = [
        {
            "id": "sig-101",
            "source": "Reddit",
            "title": "Need savory 25g protein",
            "content": "Tired of sweet protein shakes, need savory egg herb bites",
            "sector": "Food & Beverage",
            "sentiment": 0.7
        }
    ]
    out, meta = agent.process_signals(raw_signals)
    assert isinstance(out, SignalCollectorOutput)
    assert len(out.signals) >= 1
    assert out.signals[0].original_signal_id == "sig-101"
    assert meta["agent_name"] == "SignalCollectorAgent"


# ==========================================
# 4. TEST AGENT 2: TREND DETECTION (MOCKED)
# ==========================================

def test_trend_detection_agent():
    agent = TrendDetectionAgent(demo_mode=True)
    norm_output = SignalCollectorOutput(
        signals=[
            NormalizedSignal(
                original_signal_id="sig-101",
                topic="Savory Protein",
                consumer_need="Quick savory breakfast",
                sentiment=0.8,
                signal_strength=0.9,
                category="Food & Beverage",
                rationale="Savory demand"
            )
        ]
    )
    trend, meta = agent.analyze_trend(norm_output)
    assert isinstance(trend, TrendAnalysis)
    assert trend.momentum_score > 0
    assert "sig-101" in trend.supporting_signal_ids


# ==========================================
# 5. TEST AGENT 3: CONSUMER INSIGHT (MOCKED)
# ==========================================

def test_consumer_insight_agent():
    agent = ConsumerInsightAgent(demo_mode=True)
    trend = TrendAnalysis(
        trend_name="Savory High-Protein Quick Morning Formats",
        trend_description="Demand for savory morning protein",
        sector="Food & Beverage",
        momentum_score=92.0,
        confidence_score=90.0,
        growth_signal="+145% YoY",
        supporting_signal_ids=["sig-101"],
        rationale="Strong agreement",
        trend_status="EMERGING"
    )
    norm_output = SignalCollectorOutput(signals=[])
    insight, meta = agent.generate_insight(trend, norm_output)
    assert isinstance(insight, ConsumerInsight)
    assert insight.confidence_score > 0
    assert len(insight.pain_points) >= 1


# ==========================================
# 6. TEST AGENT 4: OPPORTUNITY GENERATOR (MOCKED)
# ==========================================

def test_opportunity_generator_agent():
    agent = OpportunityGeneratorAgent(demo_mode=True)
    trend = TrendAnalysis(
        trend_name="Savory High-Protein Quick Formats",
        trend_description="Savory morning protein",
        sector="Food & Beverage",
        momentum_score=92.0,
        confidence_score=90.0,
        growth_signal="+145% YoY",
        supporting_signal_ids=["sig-101"],
        rationale="Strong agreement",
        trend_status="EMERGING"
    )
    insight = ConsumerInsight(
        consumer_problem="Sweet fatigue",
        consumer_need="Savory egg bites",
        target_consumer="Urban professionals",
        jobs_to_be_done="Fast savory protein breakfast",
        motivations=["Satiety"],
        pain_points=["Nausea from sweet shakes"],
        barriers=["High retail cost"],
        desired_outcome="Sous-vide tender savory bites",
        supporting_evidence=["Reddit post"],
        confidence_score=92.0
    )
    opp, meta = agent.generate_opportunity(insight, trend)
    assert isinstance(opp, ProductOpportunity)
    assert "Protein" in opp.opportunity_title or "Savory" in opp.opportunity_title
    assert len(opp.suggested_features) >= 1


# ==========================================
# 7. TEST AGENT 5: BRAND MATCHER (MOCKED)
# ==========================================

def test_brand_matcher_agent():
    agent = BrandMatcherAgent(demo_mode=True)
    opp = ProductOpportunity(
        opportunity_title="ProBite Savory Protein Squares",
        product_concept="Sous-vide egg & cheese bites",
        product_description="High protein savory bite",
        target_consumer="Fitness enthusiasts",
        consumer_need="Quick savory protein",
        positioning="Clean savory alternative",
        differentiation="Sous-vide texture",
        suggested_features=["25g protein"],
        recommended_next_action="Pilot launch",
        expected_value="$3M ARR",
        confidence_score=94.0
    )
    brands = [
        {
            "id": str(uuid4()),
            "name": "NutriPulse",
            "sector": "Food & Beverage",
            "positioning": "High protein clean fuel",
            "target_consumer": "Fitness enthusiasts",
            "product_categories": ["Protein Snacks"]
        }
    ]
    bm, meta = agent.match_brand(opp, brands)
    assert isinstance(bm, BrandMatchResult)
    assert bm.recommended_brand_name == "NutriPulse"
    assert bm.fit_score >= 80.0


# ==========================================
# 8. TEST AGENT 6: RISK VALIDATOR (MOCKED)
# ==========================================

def test_risk_validator_agent():
    agent = RiskValidatorAgent(demo_mode=True)
    trend = TrendAnalysis(
        trend_name="Savory High-Protein Formats",
        trend_description="Savory protein demand",
        sector="Food & Beverage",
        momentum_score=90.0,
        confidence_score=90.0,
        growth_signal="+145%",
        supporting_signal_ids=["1"],
        rationale="Strong data",
        trend_status="EMERGING"
    )
    insight = ConsumerInsight(
        consumer_problem="Sweet fatigue",
        consumer_need="Savory egg bites",
        target_consumer="Urban professionals",
        jobs_to_be_done="Fast savory protein",
        motivations=["Satiety"],
        pain_points=["Rubbery texture"],
        barriers=["Cost"],
        desired_outcome="Sous-vide tender bites",
        supporting_evidence=["Reddit"],
        confidence_score=90.0
    )
    opp = ProductOpportunity(
        opportunity_title="ProBite Savory Squares",
        product_concept="Sous vide egg bites",
        product_description="Egg and herb squares",
        target_consumer="Urban professionals",
        consumer_need="Quick savory protein",
        positioning="Clean label savory",
        differentiation="Sous-vide texture",
        suggested_features=["25g protein"],
        recommended_next_action="R&D pilot",
        expected_value="$3M",
        confidence_score=92.0
    )
    bm = BrandMatchResult(
        recommended_brand_name="NutriPulse",
        fit_score=95.0,
        strategic_fit=95.0,
        category_fit=95.0,
        audience_fit=95.0,
        positioning_fit=95.0,
        capability_fit=95.0,
        alternative_brands=[],
        rationale="Perfect match"
    )
    val, meta = agent.validate_opportunity(trend, insight, opp, bm)
    assert isinstance(val, ValidationResult)
    assert val.overall_confidence > 0
    assert val.validation_status in ("APPROVED", "NEEDS_REVIEW", "REJECTED")


# ==========================================
# 9. TEST ORCHESTRATOR
# ==========================================

def test_orchestrator_pipeline_execution():
    orchestrator = PipelineOrchestrator(db=None)
    orchestrator.signal_collector.demo_mode = True
    orchestrator.trend_detector.demo_mode = True
    orchestrator.consumer_insight.demo_mode = True
    orchestrator.opportunity_generator.demo_mode = True
    orchestrator.brand_matcher.demo_mode = True
    orchestrator.risk_validator.demo_mode = True

    dummy_signals = [
        {
            "id": "sig-1",
            "source": "Reddit",
            "title": "Need savory 25g protein",
            "content": "Tired of sweet protein shakes, need savory egg herb bites",
            "sector": "Food & Beverage",
            "sentiment": 0.7
        }
    ]
    dummy_brands = [
        {
            "id": str(uuid4()),
            "name": "NutriPulse",
            "sector": "Food & Beverage",
            "positioning": "High protein clean fuel",
            "target_consumer": "Fitness enthusiasts",
            "product_categories": ["Protein Snacks"]
        }
    ]
    res = orchestrator.run_pipeline(
        scenario_name="High-Protein Breakfast",
        input_signals=dummy_signals,
        input_brands=dummy_brands
    )
    assert isinstance(res, PipelineRunResult)
    assert res.status == "completed"
    assert len(res.execution_stages) == 6
    assert res.execution_stages[0].agent_name == "SignalCollectorAgent"
    assert res.execution_stages[5].agent_name == "RiskValidatorAgent"


# ==========================================
# 10. TEST PIPELINE API ENDPOINT (POST)
# ==========================================

def test_pipeline_api_endpoint(client):
    with patch.object(PipelineOrchestrator, "run_pipeline") as mock_run:
        from agents.schemas import AgentExecutionStage
        mock_run.return_value = PipelineRunResult(
            pipeline_run_id=str(uuid4()),
            status="completed",
            scenario="High-Protein Breakfast",
            opportunity_id=str(uuid4()),
            opportunity_title="ProBite Savory Protein Squares",
            matched_brand_name="NutriPulse",
            validation_status="NEEDS_REVIEW",
            confidence_score=88.0,
            summary="High-confidence opportunity",
            execution_stages=[
                AgentExecutionStage(
                    stage_name="1. Signal Collection",
                    agent_name="SignalCollectorAgent",
                    status="SUCCESS",
                    started_at="2026-08-10T12:00:00Z",
                    completed_at="2026-08-10T12:00:02Z",
                    execution_time_ms=2000,
                    input_summary="Signals input",
                    output_summary="Normalized signals",
                    confidence_score=90.0
                ),
                AgentExecutionStage(
                    stage_name="2. Trend Detection",
                    agent_name="TrendDetectionAgent",
                    status="SUCCESS",
                    started_at="2026-08-10T12:00:02Z",
                    completed_at="2026-08-10T12:00:04Z",
                    execution_time_ms=2000,
                    input_summary="Trends input",
                    output_summary="Trend analysis",
                    confidence_score=90.0
                ),
                AgentExecutionStage(
                    stage_name="3. Consumer Insight Synthesis",
                    agent_name="ConsumerInsightAgent",
                    status="SUCCESS",
                    started_at="2026-08-10T12:00:04Z",
                    completed_at="2026-08-10T12:00:06Z",
                    execution_time_ms=2000,
                    input_summary="Insights input",
                    output_summary="JTBD synthesis",
                    confidence_score=90.0
                ),
                AgentExecutionStage(
                    stage_name="4. Opportunity Generation",
                    agent_name="OpportunityGeneratorAgent",
                    status="SUCCESS",
                    started_at="2026-08-10T12:00:06Z",
                    completed_at="2026-08-10T12:00:08Z",
                    execution_time_ms=2000,
                    input_summary="Opp input",
                    output_summary="Product concept",
                    confidence_score=90.0
                ),
                AgentExecutionStage(
                    stage_name="5. Brand Portfolio Matching",
                    agent_name="BrandMatcherAgent",
                    status="SUCCESS",
                    started_at="2026-08-10T12:00:08Z",
                    completed_at="2026-08-10T12:00:10Z",
                    execution_time_ms=2000,
                    input_summary="Brand input",
                    output_summary="Matched brand",
                    confidence_score=90.0
                ),
                AgentExecutionStage(
                    stage_name="6. Risk & Confidence Audit",
                    agent_name="RiskValidatorAgent",
                    status="SUCCESS",
                    started_at="2026-08-10T12:00:10Z",
                    completed_at="2026-08-10T12:00:12Z",
                    execution_time_ms=2000,
                    input_summary="Audit input",
                    output_summary="Validation audit",
                    confidence_score=90.0
                )
            ]
        )
        response = client.post("/api/v1/pipeline/run?scenario_name=High-Protein%20Breakfast")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["scenario"] == "High-Protein Breakfast"
        assert "execution_stages" in data
        assert len(data["execution_stages"]) == 6
