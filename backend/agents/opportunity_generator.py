"""
Opportunity Generator Agent for Think9 Pulse.
Converts consumer insights into actionable product and business opportunities.
"""

from typing import Dict, Any, Tuple, Optional
from agents.base_agent import BaseAgent
from agents.schemas import ConsumerInsight, TrendAnalysis, ProductOpportunity


class OpportunityGeneratorAgent(BaseAgent):
    def __init__(self, demo_mode: Optional[bool] = None):
        system_instruction = (
            "You are the Opportunity Generation Agent for Think9 Pulse. Your responsibility is to translate consumer insights "
            "and trend analysis into a concrete, commercial product concept proposal suitable for a consumer brand portfolio. "
            "Formulate an opportunity title, product concept, detailed description, target consumer, positioning, differentiation, "
            "suggested feature list, recommended next action, expected value tier, and feasibility confidence score. "
            "Keep concepts practical, commercially viable, and grounded in consumer demand."
        )
        super().__init__(
            agent_name="OpportunityGeneratorAgent",
            system_instruction=system_instruction,
            temperature=0.3,
            max_output_tokens=1536,
            demo_mode=demo_mode
        )

    def generate_opportunity(
        self,
        insight: ConsumerInsight,
        trend: TrendAnalysis,
        user_query: Optional[str] = None
    ) -> Tuple[ProductOpportunity, Dict[str, Any]]:
        prompt = ""
        if user_query:
            prompt += f"User Research Query: {user_query}\n\n"
        prompt += (
            f"Generate a Product Opportunity concept directly addressing the user research query based on the following insight & trend:\n\n"
            f"Trend: {trend.trend_name} ({trend.sector})\n"
            f"Consumer Problem: {insight.consumer_problem}\n"
            f"Unmet Need: {insight.consumer_need}\n"
            f"JTBD: {insight.jobs_to_be_done}\n"
            f"Desired Outcome: {insight.desired_outcome}\n"
        )

        def fallback_factory() -> ProductOpportunity:
            return ProductOpportunity(
                opportunity_title="ProBite Savory Protein Egg & Herb Breakfast Squares",
                product_concept="Sous-vide refrigerated 4-pack savory egg, Gruyère cheese, and fresh herb breakfast squares delivering 25g protein with 90-second microwave prep.",
                product_description="A premium clean-label breakfast bite crafted with cage-free eggs, aged Gruyère, chives, and sea salt. Utilizing sous-vide cooking technology to eliminate rubbery microwave textures.",
                target_consumer=insight.target_consumer,
                consumer_need=insight.consumer_need,
                positioning="The clean-label, high-protein savory alternative to sweet morning shakes and rubbery frozen bites.",
                differentiation="Sous-vide texture retention, 25g protein per serving, zero artificial gums or sodium benzoate, and savory flavor profile.",
                suggested_features=[
                    "25g Complete Protein per serving (2 squares)",
                    "Sous-vide tender texture technology",
                    "90-Second microwave heat-and-eat prep",
                    "Clean Label (No guar gum or artificial fillers)",
                    "Refrigerated 4-pack vacuum-sealed tray"
                ],
                recommended_next_action="Approve for R&D pilot formulation and execute a 1,000-unit D2C trial batch.",
                expected_value="$2.5M - $4.0M ARR initial opportunity in Year 1",
                confidence_score=94.0
            )

        return self.execute_structured(prompt, ProductOpportunity, fallback_factory)
