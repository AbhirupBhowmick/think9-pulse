"""
Trend Detection Agent for Think9 Pulse.
Clusters normalized signals into emerging trend candidates.
"""

from typing import Dict, Any, Tuple, Optional
from agents.base_agent import BaseAgent
from agents.schemas import SignalCollectorOutput, TrendAnalysis


class TrendDetectionAgent(BaseAgent):
    def __init__(self, demo_mode: Optional[bool] = None):
        system_instruction = (
            "You are the Trend Detection Agent for Think9 Pulse. "
            "Analyze normalized consumer signals and cluster them into a concise emerging trend candidate. "
            "Keep trend_description to 1-2 short sentences max. "
            "Do NOT write long essays or reproduce input signal text."
        )
        super().__init__(
            agent_name="TrendDetectionAgent",
            system_instruction=system_instruction,
            temperature=0.2,
            max_output_tokens=1024,
            demo_mode=demo_mode
        )

    def analyze_trend(self, normalized_output: SignalCollectorOutput, user_query: Optional[str] = None) -> Tuple[TrendAnalysis, Dict[str, Any]]:
        prompt = ""
        if user_query:
            prompt += f"User Query: {user_query}\n\n"
        prompt += "Analyze normalized signals and cluster them into a concise emerging trend:\n\n"
        supporting_ids = []
        for sig in normalized_output.signals:
            supporting_ids.append(sig.original_signal_id)
            prompt += (
                f"- Signal ID: {sig.original_signal_id}\n"
                f"  Topic: {sig.topic}\n"
                f"  Need: {sig.consumer_need}\n"
                f"  Category: {sig.category}\n\n"
            )

        def fallback_factory() -> TrendAnalysis:
            return TrendAnalysis(
                trend_name="Savory High-Protein Quick Morning Formats",
                trend_description="Surging consumer demand across Reddit, search queries, and TikTok for savory, non-sweet 25g+ protein breakfast bites with clean ingredients and fast microwave prep.",
                sector="Food & Beverage",
                momentum_score=92.5,
                confidence_score=91.0,
                growth_signal="+145% YoY search surge & 48M TikTok views for savory morning protein",
                supporting_signal_ids=supporting_ids,
                contradictory_signal_ids=[],
                rationale="[DEMO FALLBACK] High volume consensus across Reddit nutrition threads, search spikes, and retail feedback indicating sweet protein fatigue.",
                trend_status="EMERGING"
            )

        return self.execute_structured(prompt, TrendAnalysis, fallback_factory)
