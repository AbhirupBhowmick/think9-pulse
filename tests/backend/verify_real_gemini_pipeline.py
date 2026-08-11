"""
Real Gemini End-to-End Pipeline Execution Verification Script (Phase 4B).
Executes all 6 agents sequentially using live Gemini API calls (gemini-3-flash-preview).
"""

import os
import sys

# Ensure backend and project root are in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
backend_dir = os.path.join(project_root, "backend")
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from dotenv import load_dotenv

# Load backend/.env
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path, override=True)

from app.db.session import SessionLocal
from agents.orchestrator import PipelineOrchestrator
from agents.schemas import PipelineRunResult


def verify_real_pipeline():
    print("🚀 Initiating Real Gemini Multi-Agent End-to-End Pipeline Run (Phase 4B)...")
    print(f"Model: {os.getenv('GEMINI_MODEL_NAME')}")
    print(f"DEMO_MODE: {os.getenv('DEMO_MODE')}\n")

    db = SessionLocal()
    try:
        orchestrator = PipelineOrchestrator(db=db)
        result: PipelineRunResult = orchestrator.run_pipeline(scenario_name="High-Protein Breakfast")

        print("🎉 Real Gemini Pipeline Execution Complete!")
        print(f"Pipeline Run ID: {result.pipeline_run_id}")
        print(f"Status: {result.status}")
        print(f"Generated Opportunity Title: '{result.opportunity_title}'")
        print(f"Matched Brand: '{result.matched_brand_name}'")
        print(f"Validation Status: {result.validation_status}")
        print(f"Confidence Score: {result.confidence_score}%")
        print(f"Summary: {result.summary}\n")

        print("📊 Agent Audit Stage Execution Trace:")
        for idx, stage in enumerate(result.execution_stages, 1):
            print(f"  Stage {idx}: {stage.stage_name} ({stage.agent_name})")
            print(f"    Status: {stage.status} | Duration: {stage.execution_time_ms}ms")
            print(f"    Summary: {stage.output_summary}\n")

        assert result.status == "completed"
        assert len(result.execution_stages) == 6
        assert all(s.status == "SUCCESS" for s in result.execution_stages)
        print("✅ All 6 agents successfully executed using real Gemini API reasoning!")

        return result

    except Exception as e:
        print(f"❌ Real Gemini Pipeline Execution Failed: {type(e).__name__}: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    verify_real_pipeline()
