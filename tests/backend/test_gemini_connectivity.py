"""
Minimal Gemini API Connectivity Test for Phase 4A.
Verifies SDK import, environment variable loading, BaseAgent client initialization,
and performs ONE minimal API call without printing API keys or secrets.
"""

import os
import sys

# Ensure backend and project root are in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
backend_dir = os.path.join(project_root, "backend")
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from dotenv import load_dotenv

# Load backend/.env explicitly
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path, override=True)


def test_gemini_environment_and_connectivity():
    print("🔍 Testing Real Gemini Environment Setup...\n")

    # 1. Confirm backend/.env exists
    assert os.path.exists(env_path), f"backend/.env file not found at {env_path}"
    print("✅ 1. backend/.env file exists.")

    # 2. Confirm GEMINI_API_KEY is available (DO NOT PRINT KEY)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    assert bool(api_key), "GEMINI_API_KEY environment variable is missing or empty."
    assert api_key != "your_gemini_api_key_here", "GEMINI_API_KEY is set to placeholder text."
    print(f"✅ 2. GEMINI_API_KEY is present and configured (length: {len(api_key)} chars). [KEY REDACTED]")

    # 3. Confirm DEMO_MODE
    demo_mode = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
    print(f"ℹ️  3. DEMO_MODE setting: {demo_mode}")

    # 4. Verify google-genai SDK import
    try:
        from google import genai
        from google.genai import types
        print("✅ 4. google-genai SDK imported successfully.")
    except ImportError as e:
        raise AssertionError(f"Failed to import google-genai SDK: {e}")

    # 5. Verify BaseAgent initialization
    from agents.base_agent import BaseAgent
    agent = BaseAgent(
        agent_name="ConnectivityTestAgent",
        system_instruction="You are a system diagnostic agent. Respond concisely.",
        temperature=0.1
    )
    assert agent.client is not None, "BaseAgent failed to initialize Gemini client."
    print("✅ 5. BaseAgent successfully initialized Gemini client.")

    # 6. Perform ONE minimal Gemini API connectivity test
    print("🚀 6. Executing ONE minimal Gemini API connectivity test...")
    
    try:
        response = agent.client.models.generate_content(
            model=agent.model_name,
            contents="Respond with the word CONNECTED if you receive this message."
        )
        assert response and response.text, "Received empty response from Gemini API."
        print(f"✅ 6. Gemini API response received successfully! (Model: {agent.model_name})")
        print(f"   Output text: '{response.text.strip()}'")
        print("\n🎉 GEMINI ENVIRONMENT: READY")
        return True
    except Exception as e:
        print(f"\n❌ Gemini API test failed with error: {type(e).__name__}: {str(e)}")
        raise e


if __name__ == "__main__":
    test_gemini_environment_and_connectivity()
