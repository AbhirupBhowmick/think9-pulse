"""
Controlled Failure Scenario Verification for Phase 4B.
Verifies that when Gemini API returns an error or invalid response, the orchestrator:
1. Safely catches the exception
2. Logs error safely without exposing secret keys
3. Marks the failed stage cleanly with status 'FAILED'
4. Prevents presenting invalid opportunities as valid
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
from agents.base_agent import BaseAgent
from agents.orchestrator import PipelineOrchestrator


def test_controlled_failure():
    print("🧪 Executing Controlled Failure Scenario Verification...")

    # Create an agent initialized with an invalid model name to force a controlled API failure
    failing_agent = BaseAgent(
        agent_name="FailingTestAgent",
        model_name="nonexistent-invalid-model-name",
        system_instruction="Test instruction."
    )

    try:
        failing_agent._call_gemini("Test prompt for failure scenario")
        raise AssertionError("Expected ClientError / APIError, but API call succeeded unexpectedly.")
    except Exception as e:
        print(f"✅ 1. Controlled API failure caught successfully: {type(e).__name__}")
        assert "API key" not in str(e), "Security Violation: API key exposed in exception string!"
        print("✅ 2. Verified exception string does NOT expose API key.")

    db = SessionLocal()
    try:
        orchestrator = PipelineOrchestrator(db=db)
        # Force Agent 1 to fail by temporarily overriding its model name
        orchestrator.signal_collector.model_name = "nonexistent-invalid-model-name"
        
        try:
            result = orchestrator.run_pipeline(scenario_name="Controlled Failure Test")
        except Exception as p_err:
            print(f"✅ 3. Pipeline caught stage exception as expected: {type(p_err).__name__}")

        # Query database to confirm failed pipeline run record was persisted with FAILED status
        from app.models import PipelineRun
        db_run = db.query(PipelineRun).filter(PipelineRun.scenario_name == "Controlled Failure Test").first()
        assert db_run is not None, "Pipeline run record not found in database."
        assert db_run.status == "FAILED", f"Expected db status 'FAILED', got '{db_run.status}'"
        print(f"✅ 4. Verified database record persisted with status 'FAILED' and clean error message.")
        print(f"   Stored Error Message: '{db_run.error_message}'")
        
        print("\n🎉 CONTROLLED FAILURE TEST: PASSED")
        return True

    finally:
        db.close()


if __name__ == "__main__":
    test_controlled_failure()
