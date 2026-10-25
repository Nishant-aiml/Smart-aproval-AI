import time

def _invoke_with_backoff(call_fn, max_retries=2):
    """Retries API calls when rate-limited or congested (e.g. GLM code 1305 / 429)"""
    for attempt in range(max_retries + 1):
        try:
            return call_fn()
        except Exception as e:
            err_str = str(e)
            if ("1305" in err_str or "429" in err_str or "overloaded" in err_str.lower()) and attempt < max_retries:
                sleep_s = (attempt + 1) * 1.5
                logger.info(f"API throttled/congested (code 1305/429), retrying in {sleep_s}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(sleep_s)
                continue
            raise e

"""
AI utility functions for safe API calls (Gemini & OpenAI)
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class MockMessage:
    def __init__(self, content: str):
        self.content = content


class MockChoice:
    def __init__(self, content: str):
        self.message = MockMessage(content)


class MockChatCompletionResponse:
    def __init__(self, content: str, model: str):
        self.choices = [MockChoice(content)]
        self.model = model


def safe_openai_call(client, model: str, messages: list, timeout: int = 60, **kwargs) -> Optional[Any]:
    """
    Safely call AI API (Gemini or OpenAI) with multiple fallback strategies.
    Handles temperature, response_format, and model fallbacks cleanly.
    """
    if client is None:
        # Try direct native GeminiClient as a seamless fallback
        try:
            from ai.gemini_client import GeminiClient
            gemini = GeminiClient()
            if gemini.available:
                logger.info("OpenAI client not provided; delegating call to native GeminiClient")
                json_mode = kwargs.get("response_format", {}).get("type") == "json_object" if isinstance(kwargs.get("response_format"), dict) else False
                temp = kwargs.get("temperature", 0.1)

                prompt_parts = []
                system_instruction = None
                for m in messages:
                    if m.get("role") == "system":
                        system_instruction = m.get("content")
                    else:
                        prompt_parts.append(m.get("content", ""))
                prompt_text = "\n\n".join(prompt_parts)

                result_text = gemini.generate_text(
                    prompt=prompt_text,
                    system_prompt=system_instruction,
                    temperature=temp,
                    json_mode=json_mode,
                    timeout=timeout
                )
                return MockChatCompletionResponse(result_text, model=gemini.model_name)
        except Exception as e:
            logger.warning(f"Native Gemini fallback failed: {e}")

        raise ValueError("AI client is not initialized. Please configure GEMINI_API_KEY in your .env file.")

    # Strategy 1: Try with all provided parameters
    try:
        return _invoke_with_backoff(lambda: client.chat.completions.create(
            model=model,
            messages=messages,
            timeout=timeout,
            **kwargs)
        )
    except Exception as e1:
        logger.debug(f"Strategy 1 (full params) failed: {e1}")

    # Strategy 2: Try without temperature (some models/endpoints have constraints)
    if "temperature" in kwargs:
        try:
            call_kwargs = {k: v for k, v in kwargs.items() if k != "temperature"}
            return _invoke_with_backoff(lambda: client.chat.completions.create(
                model=model,
                messages=messages,
                timeout=timeout,
                **call_kwargs)
            )
        except Exception as e2:
            logger.debug(f"Strategy 2 (no temperature) failed: {e2}")

    # Strategy 3: Try without response_format
    if "response_format" in kwargs:
        try:
            call_kwargs = {k: v for k, v in kwargs.items() if k != "response_format"}
            return _invoke_with_backoff(lambda: client.chat.completions.create(
                model=model,
                messages=messages,
                timeout=timeout,
                **call_kwargs)
            )
        except Exception as e3:
            logger.debug(f"Strategy 3 (no response_format) failed: {e3}")

    # Strategy 4: Minimal parameters - just model, messages, timeout
    try:
        return _invoke_with_backoff(lambda: client.chat.completions.create(
            model=model,
            messages=messages,
            timeout=timeout)
        )
    except Exception as e4:
        # Strategy 5: Native GeminiClient fallback
        try:
            from ai.gemini_client import GeminiClient
            gemini = GeminiClient()
            if gemini.available:
                logger.info("Endpoint call failed; falling back to native GeminiClient...")
                json_mode = kwargs.get("response_format", {}).get("type") == "json_object" if isinstance(kwargs.get("response_format"), dict) else False
                temp = kwargs.get("temperature", 0.1)
                prompt_parts = [m.get("content", "") for m in messages if m.get("role") != "system"]
                system_instruction = next((m.get("content") for m in messages if m.get("role") == "system"), None)
                result_text = gemini.generate_text(
                    prompt="\n\n".join(prompt_parts),
                    system_prompt=system_instruction,
                    temperature=temp,
                    json_mode=json_mode,
                    timeout=timeout
                )
                return MockChatCompletionResponse(result_text, model=gemini.model_name)
        except Exception as e5:
            logger.debug(f"Native Gemini fallback also failed: {e5}")

        logger.error(f"All AI call strategies failed: {e4}")
        raise e4
