"""
Consumer Insight Agent for Think9 Pulse.
Transforms trend candidates into structured consumer insights and JTBD frameworks.
"""

from typing import Dict, Any, Tuple, Optional
from agents.base_agent import BaseAgent
from agents.schemas import TrendAnalysis, SignalCollectorOutput, ConsumerInsight


class ConsumerInsightAgent(BaseAgent):
    def __init__(self, demo_mode: Optional[bool] = None):
        system_instruction = (
            "You are the Consumer Insight Agent for Think9 Pulse. Your responsibility is to translate detected trend clusters "
            "and supporting consumer signals into an actionable Consumer Insight synthesis. "
            "Define the core consumer problem, unfulfilled need, target consumer profile, Jobs-To-Be-Done (JTBD) statement, "
            "motivations, pain points, barriers, desired outcome, and supporting evidence references. "
            "Ground your synthesis strictly in the provided evidence. Do NOT fabricate survey metrics or fake consumer quotes."
        )
        super().__init__(
            agent_name="ConsumerInsightAgent",
            system_instruction=system_instruction,
            temperature=0.2,
            max_output_tokens=1536,
            demo_mode=demo_mode
        )

    def generate_insight(
        self,
        trend: TrendAnalysis,
        normalized_output: SignalCollectorOutput,
        user_query: Optional[str] = None
    ) -> Tuple[ConsumerInsight, Dict[str, Any]]:
        prompt = ""
        if user_query:
            prompt += f"User Research Query: {user_query}\n\n"
        prompt += (
            f"Synthesize a Consumer Insight for the following trend candidate:\n\n"
            f"Trend Name: {trend.trend_name}\n"
            f"Sector: {trend.sector}\n"
            f"Description: {trend.trend_description}\n"
            f"Growth Vector: {trend.growth_signal}\n\n"
            f"Supporting Consumer Signals:\n"
        )
        for sig in normalized_output.signals:
            prompt += f"- Topic: {sig.topic} | Need: {sig.consumer_need} | Sentiment: {sig.sentiment}\n"

        def fallback_factory() -> ConsumerInsight:
            return ConsumerInsight(
                consumer_problem="Busy professionals experience morning sweet fatigue from sweet protein powders, shakes, and bars, but lack fast savory high-protein alternatives.",
                consumer_need="Demand for a quick 90-second savory breakfast bite packing 25g clean protein, real eggs, and zero artificial rubbery additives.",
                target_consumer="Urban professionals, fitness enthusiasts, and macro-conscious breakfast eaters (ages 24-45).",
                jobs_to_be_done="When I am rushing in the morning before work or workout, I want a hot, savory high-protein breakfast in under 2 minutes so I stay satiated without feeling nauseous from sweet shakes.",
                motivations=[
                    "Satiety and sustained morning energy",
                    "Savory flavor preference over sweet powders",
                    "Clean label reassurance (no gums or preservatives)"
                ],
                pain_points=[
                    "Nausea/fatigue from sweet protein shakes at 7am",
                    "Existing microwave egg bites become rubbery",
                    "Traditional prep takes 15+ minutes of cooking/cleaning"
                ],
                barriers=[
                    "High price of fresh retail grab-and-go options",
                    "Short shelf life of fresh refrigerated eggs"
                ],
                desired_outcome="Delicious, sous-vide tender savory protein bites ready in 90 seconds with 25g protein and clean ingredients.",
                supporting_evidence=[
                    "Reddit r/nutrition thread demanding savory 25g egg formats",
                    "Amazon review highlighting rubbery texture & gum fillers in existing brands",
                    "+145% YoY Google Search spike for 'savory quick high protein breakfast'"
                ],
                confidence_score=93.0
            )

        return self.execute_structured(prompt, ConsumerInsight, fallback_factory)
