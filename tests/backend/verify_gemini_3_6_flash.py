"""
Phase 5A Verification Script for Gemini 3.6 Flash.
Verifies:
1. Connectivity with model 'gemini-3.6-flash'.
2. Structured Pydantic JSON output using 'gemini-3.6-flash'.
3. Complete 6-agent pipeline execution using 'gemini-3.6-flash'.
"""

import os
import sys
import logging
from pydantic import BaseModel, Field

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)
backend_path = os.path.join(project_root, "backend")
sys.path.insert(0, backend_path)

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(backend_path, ".env"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verify-gemini-3-6-flash")

class ConnectivitySchema(BaseModel):
    status: str = Field(description="Status string e.g. READY")
    model_used: str = Field(description="Exact model name used")
    reasoning_check: str = Field(description="Brief confirmation message")

def verify_gemini_3_6():
    print("==================================================")
    print("🚀 PHASE 5A: GEMINI 3.6 FLASH VERIFICATION")
    print("==================================================")
    
    model_configured = os.getenv("GEMINI_MODEL_NAME", "NOT SET")
    api_key = os.getenv("GEMINI_API_KEY", "")
    demo_mode = os.getenv("DEMO_MODE", "true")
    
    print(f"MODEL CONFIGURED: {model_configured}")
    print(f"DEMO_MODE: {demo_mode}")
    print(f"API KEY SET: {'YES' if api_key and api_key != 'your_gemini_api_key_here' else 'NO'}")
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ Error: GEMINI_API_KEY is missing or invalid.")
        sys.exit(1)
        
    from agents.base_agent import BaseAgent
    from agents.orchestrator import PipelineOrchestrator
    from backend.app.db.session import SessionLocal
    
    # 1. Minimal Connectivity & Structured Output Test
    agent = BaseAgent(
        agent_name="TestAgent",
        system_instruction="You are a system health diagnostic assistant. Return structured output.",
        model_name="gemini-3.6-flash",
        demo_mode=False
    )
    
    print("\n--- 1. Testing Gemini 3.6 Flash Structured Output ---")
    try:
        res, meta = agent.execute_structured(
            prompt="Verify system connectivity and confirm model name is gemini-3.6-flash.",
            schema_class=ConnectivitySchema
        )
        print(f"✅ GEMINI 3.6 CONNECTIVITY: SUCCESS")
        print(f"✅ STRUCTURED OUTPUT: SUCCESS")
        print(f"   Model Actually Used: {meta.get('model')}")
        print(f"   Status Output: {res.status}")
        print(f"   Reasoning: {res.reasoning_check}")
    except Exception as e:
        print(f"❌ GEMINI 3.6 CONNECTIVITY FAILED: {e}")
        sys.exit(1)

    # 2. Run 6-Agent End-to-End Pipeline
    print("\n--- 2. Testing Complete 6-Agent Pipeline with Gemini 3.6 Flash ---")
    db = SessionLocal()
    try:
        orchestrator = PipelineOrchestrator(db=db)
        result = orchestrator.run_pipeline(scenario_name="High-Protein Breakfast")
        
        print("\n🎉 6-Agent Pipeline Run Complete!")
        print(f"Pipeline Run ID: {result.pipeline_run_id}")
        print(f"Status: {result.status}")
        print(f"Opportunity Title: '{result.opportunity.title if result.opportunity else 'N/A'}'")
        print(f"Matched Brand: '{result.opportunity.brand.name if result.opportunity and result.opportunity.brand else 'N/A'}'")
        print(f"Validation Status: {result.opportunity.status if result.opportunity else 'N/A'}")
        print(f"Confidence Score: {result.opportunity.confidence_score if result.opportunity else 'N/A'}%")
        
        # Verify that all 6 stages used gemini-3.6-flash and no fallback was used
        print("\n📊 Stage Model Verification:")
        all_gemini_3_6 = True
        no_fallbacks = True
        
        for stage in result.execution_stages:
            model_used = stage.model_used
            is_fallback = stage.is_fallback
            print(f"  Stage {stage.stage_number} ({stage.stage_name}): model={model_used}, fallback={is_fallback}")
            if "gemini-3.6-flash" not in model_used:
                all_gemini_3_6 = False
            if is_fallback:
                no_fallbacks = False
                
        print(f"\nALL AGENTS USED GEMINI 3.6 FLASH: {all_gemini_3_6}")
        print(f"FALLBACK USED: {not no_fallbacks}")
        
    except Exception as e:
        print(f"❌ 6-Agent Pipeline Execution Failed: {e}")
        db.close()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    verify_gemini_3_6()
