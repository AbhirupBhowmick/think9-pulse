"""
Base Agent Class for Think9 Pulse Multi-Agent Pipeline.
Provides standardized Gemini API execution, structured JSON output validation,
retry mechanics, error handling, timing metrics, and demo fallback capabilities.
"""

import logging
import os
import time
from datetime import datetime, timezone
from typing import Type, TypeVar, Optional, Dict, Any, Tuple
from pydantic import BaseModel

try:
    from app.core.config import settings
except ImportError:
    settings = None

logger = logging.getLogger("think9-pulse.agent")

T = TypeVar("T", bound=BaseModel)

# Check google-genai SDK availability
try:
    from google import genai
    from google.genai import types
    HAS_GENAI_SDK = True
except ImportError:
    HAS_GENAI_SDK = False
    logger.warning("google-genai SDK not installed. Falling back to structured demo mode.")


class BaseAgent:
    def __init__(
        self,
        agent_name: str,
        system_instruction: str,
        model_name: Optional[str] = None,
        temperature: float = 0.2,
        max_output_tokens: int = 8192,
        timeout: int = 30,
        retry_count: int = 4,
        thinking_level: Optional[str] = None,
        demo_mode: Optional[bool] = None
    ):
        self.agent_name = agent_name
        self.system_instruction = system_instruction
        
        default_model = (getattr(settings, "GEMINI_MODEL_NAME", None) if settings else None) or "gemini-3.6-flash"
        self.model_name = model_name or os.getenv("GEMINI_MODEL_NAME", default_model)
        self.temperature = float(os.getenv("GEMINI_TEMPERATURE", temperature))
        self.max_output_tokens = int(os.getenv("GEMINI_MAX_TOKENS", max_output_tokens or 8192))
        self.timeout = timeout
        self.retry_count = retry_count
        self.thinking_level = thinking_level
        self.demo_mode = demo_mode if demo_mode is not None else (os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "yes"))

        # Initialize Gemini Client if API Key is set
        key_from_settings = getattr(settings, "GEMINI_API_KEY", "") if settings else ""
        self.api_key = (os.getenv("GEMINI_API_KEY") or key_from_settings or "").strip()
        self.client = None
        
        if self.api_key and self.api_key != "your_gemini_api_key_here" and HAS_GENAI_SDK:
            try:
                self.client = genai.Client(api_key=self.api_key)
                logger.info(f"[{self.agent_name}] Initialized Gemini API Client with model '{self.model_name}'")
            except Exception as e:
                logger.error(f"[{self.agent_name}] Failed to initialize Gemini client: {e}")
                self.client = None

    def execute_structured(
        self,
        prompt: str,
        schema_class: Type[T],
        fallback_factory: Optional[callable] = None
    ) -> Tuple[T, Dict[str, Any]]:
        """
        Executes a prompt against Gemini API expecting a structured JSON response matching schema_class.
        Returns (parsed_pydantic_object, execution_metadata).
        """
        start_time = time.time()
        started_at = datetime.now(timezone.utc).isoformat()
        
        # If Gemini client is available, attempt API call
        if self.client:
            for attempt in range(1, self.retry_count + 2):
                try:
                    logger.info(f"[{self.agent_name}] Sending prompt to Gemini API (Attempt {attempt})...")
                    
                    thinking_cfg = types.ThinkingConfig(thinking_level=self.thinking_level) if (self.thinking_level and HAS_GENAI_SDK) else None
                    
                    config = types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        max_output_tokens=self.max_output_tokens,
                        response_mime_type="application/json",
                        response_schema=schema_class,
                        thinking_config=thinking_cfg
                    )
                    
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config=config
                    )
                    
                    if not response:
                        raise ValueError("No response object returned from Gemini API.")

                    # Inspect finish reason for token truncation
                    if getattr(response, "candidates", None):
                        candidate = response.candidates[0]
                        finish_reason = getattr(candidate, "finish_reason", None)
                        finish_reason_str = str(finish_reason).upper() if finish_reason else ""
                        if "MAX_TOKENS" in finish_reason_str or "LENGTH" in finish_reason_str:
                            logger.error(f"[{self.agent_name}] Gemini output truncated due to output token limit.")
                            raise ValueError(f"[{self.agent_name}] Incomplete structured JSON returned (truncated by MAX_TOKENS).")

                    if not response.text:
                        raise ValueError("Empty text response received from Gemini API.")
                    
                    parsed_result = schema_class.model_validate_json(response.text)
                    execution_time_ms = int((time.time() - start_time) * 1000)
                    completed_at = datetime.now(timezone.utc).isoformat()
                    
                    meta = {
                        "agent_name": self.agent_name,
                        "model": self.model_name,
                        "status": "SUCCESS",
                        "started_at": started_at,
                        "completed_at": completed_at,
                        "execution_time_ms": execution_time_ms,
                        "attempts": attempt,
                        "is_fallback": False
                    }
                    logger.info(f"[{self.agent_name}] Successfully executed in {execution_time_ms}ms")
                    return parsed_result, meta

                except Exception as exc:
                    err_msg = str(exc)
                    logger.warning(f"[{self.agent_name}] API execution attempt {attempt} failed: {err_msg}")
                    
                    # Rate limit (429) backoff retry
                    if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                        if attempt < self.retry_count:
                            logger.info(f"[{self.agent_name}] Free tier rate limit (429) encountered. Pausing 6 seconds before retry...")
                            time.sleep(6.0)
                            continue
                    
                    # Non-retryable error (e.g. JSON truncation or validation failure)
                    logger.error(f"[{self.agent_name}] Non-retryable API error encountered.")
                    if not self.demo_mode:
                        raise RuntimeError(f"[{self.agent_name}] Gemini API call failed: {err_msg}")

        # Fallback handling if API key missing or API call fails
        execution_time_ms = int((time.time() - start_time) * 1000)
        completed_at = datetime.now(timezone.utc).isoformat()
        
        if fallback_factory and self.demo_mode:
            logger.info(f"[{self.agent_name}] Utilizing controlled demo fallback response.")
            fallback_result = fallback_factory()
            meta = {
                "agent_name": self.agent_name,
                "model": f"{self.model_name} (DEMO FALLBACK)",
                "status": "DEMO_FALLBACK",
                "started_at": started_at,
                "completed_at": completed_at,
                "execution_time_ms": execution_time_ms,
                "attempts": 0,
                "is_fallback": True,
                "note": "DEMO FALLBACK — NOT GENERATED BY GEMINI"
            }
            return fallback_result, meta

        raise RuntimeError(f"[{self.agent_name}] Execution failed and no fallback available. Gemini API key required.")
