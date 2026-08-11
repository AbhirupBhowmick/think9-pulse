"""
Risk / Confidence Validation Agent for Think9 Pulse.
Acts as a critical auditor challenging generated opportunities and brand matches.
"""

from typing import Dict, Any, Tuple, Optional
from agents.base_agent import BaseAgent
from agents.schemas import (
    TrendAnalysis, ConsumerInsight, ProductOpportunity,
    BrandMatchResult, ValidationResult, RiskFactor
)


class RiskValidatorAgent(BaseAgent):
    def __init__(self, demo_mode: Optional[bool] = None):
        system_instruction = (
            "You are the Risk / Confidence Validation Agent for Think9 Pulse. Your responsibility is to serve as a critical, "
            "rigorous business auditor. Do NOT blindly agree with preceding agents. Audit the opportunity for evidence sufficiency, "
            "trend longevity vs fad risk, competitive landscape, regulatory compliance, cold-chain supply complexity, and margin viability. "
            "Output composite overall_confidence score (0-100), individual sub-scores (evidence_score, trend_reliability_score, brand_fit_score, "
            "feasibility_score, risk_score), identified_risks list with severity, missing_information items, validation_status "
            "('APPROVED', 'NEEDS_REVIEW', or 'REJECTED'), recommended executive action, and a concise validation summary."
        )
        super().__init__(
            agent_name="RiskValidatorAgent",
            system_instruction=system_instruction,
            temperature=0.1,
            max_output_tokens=1536,
            demo_mode=demo_mode
        )

    def validate_opportunity(
        self,
        trend: TrendAnalysis,
        insight: ConsumerInsight,
        opportunity: ProductOpportunity,
        brand_match: BrandMatchResult
    ) -> Tuple[ValidationResult, Dict[str, Any]]:
        prompt = (
            f"Perform a critical business audit on the following opportunity candidate:\n\n"
            f"Trend: {trend.trend_name} (Momentum: {trend.momentum_score}, Growth: {trend.growth_signal})\n"
            f"Consumer Problem: {insight.consumer_problem}\n"
            f"Opportunity Title: {opportunity.opportunity_title}\n"
            f"Product Concept: {opportunity.product_concept}\n"
            f"Matched Brand: {brand_match.recommended_brand_name} (Fit Score: {brand_match.fit_score})\n"
        )

        def fallback_factory() -> ValidationResult:
            return ValidationResult(
                overall_confidence=91.0,
                evidence_score=92.0,
                trend_reliability_score=89.0,
                brand_fit_score=95.0,
                feasibility_score=88.0,
                risk_score=18.0,
                identified_risks=[
                    RiskFactor(
                        category="Supply Chain",
                        severity="Medium",
                        description="Requires refrigerated sous-vide manufacturing line and cold-chain distribution logistics."
                    ),
                    RiskFactor(
                        category="Competitive",
                        severity="Low",
                        description="Legacy incumbents offer frozen egg bites, but clean-label sous-vide refrigerated format remains uncluttered."
                    )
                ],
                missing_information=[
                    "COGS breakdown for 4-pack sous-vide packaging at scale",
                    "Refrigerated shelf-life testing results (target 45 days)"
                ],
                validation_status="NEEDS_REVIEW",
                recommended_action="Approve for NutriPulse pilot batch contingent on 45-day shelf-life stability test.",
                validation_summary="[DEMO FALLBACK] High-confidence opportunity (91%) backed by multi-channel signal consensus. Cold-chain distribution is the primary operational risk to validate during pilot phase."
            )

        return self.execute_structured(prompt, ValidationResult, fallback_factory)
