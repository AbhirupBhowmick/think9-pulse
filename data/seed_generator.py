"""
Seed Data Generator for Think9 Pulse
Populates database with representative simulated brands, signals, trends, evidence, and opportunities.
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.brand import Brand
from app.models.signal import Signal
from app.models.trend import Trend
from app.models.evidence import Evidence
from app.models.opportunity import Opportunity
from app.models.pipeline_run import PipelineRun


def load_json_data(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_database():
    print("🌱 Initializing Think9 Pulse Database Schema & Seed Data...")

    # Create tables if not exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        existing_brands = db.query(Brand).count()
        if existing_brands > 0:
            print(f"⚠️  Database already contains {existing_brands} brands. Re-seeding clean state...")
            db.query(Evidence).delete()
            db.query(Opportunity).delete()
            db.query(Trend).delete()
            db.query(Signal).delete()
            db.query(Brand).delete()
            db.query(PipelineRun).delete()
            db.commit()

        # 1. Seed Brands
        data_dir = os.path.dirname(__file__)
        brands_data = load_json_data(os.path.join(data_dir, "think9_brands.json"))
        brand_map = {}

        for b in brands_data:
            brand_obj = Brand(
                id=uuid.uuid4(),
                name=b["name"],
                sector=b["sector"],
                description=b["description"],
                target_consumer=b["target_consumer"],
                positioning=b["positioning"],
                product_categories=b["product_categories"]
            )
            db.add(brand_obj)
            brand_map[b["name"]] = brand_obj

        db.commit()
        print(f"✅ Seeded {len(brands_data)} Think9 portfolio brands.")

        # 2. Seed Signals
        signals_data = load_json_data(os.path.join(data_dir, "raw_signals.json"))
        signal_objs = []
        flagship_signals = []

        for s in signals_data:
            sig_obj = Signal(
                id=uuid.uuid4(),
                source=s["source"],
                source_url=s.get("source_url"),
                title=s.get("title"),
                content=s["content"],
                signal_type=s["signal_type"],
                sector=s["sector"],
                sentiment=s.get("sentiment", 0.0),
                signal_strength=s.get("signal_strength", 0.5),
                geography=s.get("geography", "US/Global"),
                metadata_=s.get("metadata", {}),
                embedding=None
            )
            db.add(sig_obj)
            signal_objs.append(sig_obj)

            if s.get("metadata", {}).get("flagship_scenario") == "High-Protein Breakfast":
                flagship_signals.append(sig_obj)

        db.commit()
        print(f"✅ Seeded {len(signals_data)} representative consumer signals.")

        # 3. Seed Flagship Trend: "Savory High-Protein Quick Morning Formats"
        flagship_trend = Trend(
            id=uuid.uuid4(),
            name="Savory High-Protein Quick Morning Formats",
            description="SIMULATED DEMO TREND: Surging consumer demand for savory, non-sweet breakfast formats packing 25g+ clean protein with under 3 minutes prep time.",
            sector="Food & Beverage",
            momentum_score=92.5,
            confidence_score=91.0,
            growth_rate=145.0, # +145% YoY
            signal_count=len(flagship_signals),
            status="EMERGING"
        )
        db.add(flagship_trend)
        db.commit()
        print(f"✅ Seeded flagship trend: '{flagship_trend.name}'")

        # 4. Seed Evidence Records
        evidence_explanations = [
            ("DIRECT_MENTION", 0.95, "Consumer Reddit post directly articulates sweet protein fatigue and explicit request for savory 25g egg herb bite format."),
            ("CRITIQUE_ANALYSIS", 0.88, "Amazon review confirms existing market products suffer from rubbery microwave texture and excessive artificial gums."),
            ("SEARCH_SPIKE", 0.96, "Google Search trends confirm +145% YoY velocity surge for 'savory quick high protein breakfast'."),
            ("SOCIAL_VIRALITY", 0.90, "TikTok hashtag #SavoryProteinBreakfast reached 48M views with high engagement among 22-38 demographic."),
            ("RETAIL_GAP", 0.84, "Target/Whole Foods category buyer notes 30% surge in fresh refrigerated morning protein demand with lack of savory offerings.")
        ]

        for i, sig in enumerate(flagship_signals):
            ev_type, score, exp = evidence_explanations[i % len(evidence_explanations)]
            ev_obj = Evidence(
                id=uuid.uuid4(),
                trend_id=flagship_trend.id,
                signal_id=sig.id,
                evidence_type=ev_type,
                relevance_score=score,
                explanation=f"[SIMULATED EVIDENCE] {exp}"
            )
            db.add(ev_obj)

        db.commit()
        print(f"✅ Seeded {len(flagship_signals)} evidence relationships.")

        # 5. Seed Flagship Opportunity: "ProBite Savory Protein Egg & Herb Breakfast Squares"
        nutripulse_brand = brand_map.get("NutriPulse")

        flagship_opportunity = Opportunity(
            id=uuid.uuid4(),
            trend_id=flagship_trend.id,
            brand_id=nutripulse_brand.id if nutripulse_brand else None,
            title="ProBite Savory Protein Egg & Herb Breakfast Squares",
            description="SIMULATED DEMO OPPORTUNITY: Ready-to-heat sous-vide egg, Gruyère cheese, and fresh herb breakfast squares providing 25g protein, 2g net carbs, and clean label formulation.",
            consumer_need="Urban professionals seek a quick 2-minute savory breakfast rich in protein without sweet taste fatigue or rubbery microwave texture.",
            target_consumer="Fitness enthusiasts, busy executives, and macro-conscious consumers (ages 24-45).",
            product_concept="Sous-vide refrigerated 4-pack breakfast bites ($16.99 MSRP) made with cage-free eggs, sharp cheese, and chives. 90-second microwave prep.",
            positioning="The clean-label, high-protein savory alternative to sweet morning shakes and rubbery frozen bites.",
            confidence_score=94.0,
            risk_score=18.0,
            status="IN_REVIEW",
            source_type="seed",
            recommended_action="Approve for NutriPulse R&D pilot batch and launch 1,000-unit D2C trial in Q4."
        )
        db.add(flagship_opportunity)
        db.commit()
        print(f"✅ Seeded flagship opportunity: '{flagship_opportunity.title}' matched to brand '{nutripulse_brand.name if nutripulse_brand else 'N/A'}'")

        # 6. Seed Pipeline Run Record
        pipeline_run = PipelineRun(
            id=uuid.uuid4(),
            scenario_name="High-Protein Breakfast",
            user_query="SIMULATED DEMO: Find unmet demand for quick healthy breakfast products",
            status="COMPLETED",
            source_type="seed",
            current_stage="COMPLETED",
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
            error_message=None
        )
        db.add(pipeline_run)
        db.commit()
        print(f"✅ Seeded pipeline run execution log.")

        print("🎉 Database successfully seeded!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
