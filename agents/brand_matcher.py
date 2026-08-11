"""
Brand Matcher Agent for Think9 Pulse.
Matches product opportunities with the optimal Think9 portfolio brand.
"""

from typing import List, Dict, Any, Tuple, Optional
from agents.base_agent import BaseAgent
from agents.schemas import ProductOpportunity, BrandMatchResult


class BrandMatcherAgent(BaseAgent):
    def __init__(self, demo_mode: Optional[bool] = None):
        system_instruction = (
            "You are the Brand Matching Agent for Think9 Pulse. Your responsibility is to evaluate a generated product opportunity "
            "against Think9's portfolio brand profiles. Compare the opportunity's sector, positioning, target audience, and concept "
            "with each available brand. Select the best-fit brand, assign an overall fit_score (0-100), strategic_fit, category_fit, "
            "audience_fit, positioning_fit, capability_fit, identify alternative brand candidates, and detail analytical rationale. "
            "Do NOT invent brands outside the supplied portfolio list."
        )
        super().__init__(
            agent_name="BrandMatcherAgent",
            system_instruction=system_instruction,
            temperature=0.1,
            max_output_tokens=2048,
            thinking_level="minimal",
            demo_mode=demo_mode
        )

    def match_brand(
        self,
        opportunity: ProductOpportunity,
        available_brands: List[Dict[str, Any]]
    ) -> Tuple[BrandMatchResult, Dict[str, Any]]:
        prompt = (
            f"Evaluate the following Product Opportunity against Think9's Brand Portfolio:\n\n"
            f"Opportunity Title: {opportunity.opportunity_title}\n"
            f"Concept: {opportunity.product_concept}\n"
            f"Target Consumer: {opportunity.target_consumer}\n"
            f"Positioning: {opportunity.positioning}\n\n"
            f"Think9 Portfolio Brands:\n"
        )
        for b in available_brands:
            prompt += (
                f"- Brand ID: {b.get('id')}\n"
                f"  Name: {b.get('name')}\n"
                f"  Sector: {b.get('sector')}\n"
                f"  Positioning: {b.get('positioning')}\n"
                f"  Target Audience: {b.get('target_consumer')}\n"
                f"  Categories: {b.get('product_categories')}\n\n"
            )

        def fallback_factory() -> BrandMatchResult:
            # Find NutriPulse or first Food & Beverage brand
            matched_brand = None
            for b in available_brands:
                if b.get("name") == "NutriPulse" or b.get("sector") == "Food & Beverage":
                    matched_brand = b
                    break
            
            if not matched_brand and available_brands:
                matched_brand = available_brands[0]

            matched_id = str(matched_brand.get("id")) if matched_brand else None
            matched_name = matched_brand.get("name", "NutriPulse") if matched_brand else "NutriPulse"

            return BrandMatchResult(
                recommended_brand_id=matched_id,
                recommended_brand_name=matched_name,
                fit_score=95.0,
                strategic_fit=96.0,
                category_fit=98.0,
                audience_fit=94.0,
                positioning_fit=92.0,
                capability_fit=95.0,
                alternative_brands=["VitalHydrate"],
                rationale=f"[DEMO FALLBACK] '{matched_name}' is the premier functional nutrition brand in Think9's portfolio, with 100% alignment in high-protein formats and active urban demographics."
            )

        return self.execute_structured(prompt, BrandMatchResult, fallback_factory)
