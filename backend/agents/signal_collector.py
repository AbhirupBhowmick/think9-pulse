"""
Signal Collector Agent for Think9 Pulse.
Normalizes raw multi-channel consumer signals into structured records.
"""

from typing import List, Dict, Any, Tuple, Optional
from agents.base_agent import BaseAgent
from agents.schemas import SignalCollectorOutput, NormalizedSignal


class SignalCollectorAgent(BaseAgent):
    def __init__(self, demo_mode: Optional[bool] = None):
        system_instruction = (
            "You are the Signal Collector Agent for Think9 Pulse. "
            "Analyze raw consumer signals and extract concise normalization metrics. "
            "Keep topics under 8 words and consumer needs to 1 short sentence max. "
            "Do NOT write long paragraphs or reproduce full raw signal text. Preserve original signal IDs."
        )
        super().__init__(
            agent_name="SignalCollectorAgent",
            system_instruction=system_instruction,
            temperature=0.1,
            max_output_tokens=4096,
            thinking_level="minimal",
            demo_mode=demo_mode
        )

    def process_signals(self, raw_signals: List[Dict[str, Any]], user_query: Optional[str] = None) -> Tuple[SignalCollectorOutput, Dict[str, Any]]:
        prompt = ""
        if user_query:
            prompt += f"User Query: {user_query}\n\n"
        prompt += "Normalize raw signals into concise structured records:\n\n"
        for i, sig in enumerate(raw_signals, 1):
            content_snippet = str(sig.get('content', ''))[:150]
            prompt += (
                f"Signal #{i} (ID: {sig.get('id')}):\n"
                f"- Source: {sig.get('source')}\n"
                f"- Title: {sig.get('title', 'N/A')}\n"
                f"- Snippet: {content_snippet}\n"
                f"- Sector: {sig.get('sector')}\n\n"
            )

        def fallback_factory() -> SignalCollectorOutput:
            normalized_list = []
            for sig in raw_signals:
                sig_id = str(sig.get("id"))
                content = sig.get("content", "")
                title = sig.get("title", "")
                
                if "savory" in content.lower() or "protein" in content.lower():
                    topic = "Savory High-Protein Breakfast Formats"
                    need = "Demand for quick, savory 25g+ protein breakfast bites without sweet taste fatigue or artificial gums."
                    category = "Food & Beverage"
                    entities = ["Protein Snacks", "Sous-Vide Bites", "Egg & Herb Formats"]
                elif "barrier" in content.lower() or "skin" in content.lower():
                    topic = "Bio-Fermented Barrier Repair Skincare"
                    need = "Demand for postbiotic skincare formulations that soothe sensitive skin without synthetic fillers."
                    category = "Skincare & Personal Care"
                    entities = ["Barrier Repair Cream", "Postbiotics", "Bio-ferments"]
                else:
                    topic = title or "Consumer Feedback"
                    need = content[:100]
                    category = sig.get("sector", "General")
                    entities = []

                normalized_list.append(
                    NormalizedSignal(
                        original_signal_id=sig_id,
                        topic=topic,
                        consumer_need=need,
                        sentiment=float(sig.get("sentiment", 0.0)),
                        signal_strength=float(sig.get("signal_strength", 0.8)),
                        category=category,
                        geographic_relevance=sig.get("geography", "US/Global"),
                        key_entities=entities,
                        rationale=f"[DEMO FALLBACK] Normalized from raw signal ID {sig_id}"
                    )
                )
            return SignalCollectorOutput(signals=normalized_list)

        return self.execute_structured(prompt, SignalCollectorOutput, fallback_factory)
