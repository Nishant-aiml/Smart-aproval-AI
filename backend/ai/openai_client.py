"""
AI client wrapper supporting Gemini (Primary - Gemini 1.5 Flash) and OpenAI.
Maintains full backward compatibility for all block classification, extraction, and chat methods.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
import openai
from config.settings import settings
from utils.validators import sanitize_json_string, parse_json_safely
from ai.openai_utils import safe_openai_call
from ai.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Unified AI Client.
    Defaults to Gemini (Gemini 1.5 Flash - fastest, cheapest free tier).
    Supports drop-in OpenAI compatibility across the entire system.
    """

    def __init__(self):
        gemini_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        openai_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        glm_key = getattr(settings, "GLM_API_KEY", None) or os.getenv("GLM_API_KEY")
        glm_base_url = getattr(settings, "GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
        glm_model = getattr(settings, "GLM_MODEL", "GLM-4.7-Flash")
        glm_fallback = getattr(settings, "GLM_MODEL_FALLBACK", "GLM-4.7-Flash")
        provider = getattr(settings, "AI_PROVIDER", "glm").lower()

        self.native_gemini = GeminiClient()

        if provider == "glm" and glm_key:
            self.provider = "glm"
            self.primary_model = glm_model
            self.fallback_model = glm_fallback
            try:
                self.client = openai.OpenAI(
                    api_key=glm_key,
                    base_url=glm_base_url
                )
                logger.info(f"AI Client configured with GLM (OpenAI-compatible) - Model: {self.primary_model} at {glm_base_url}")
            except Exception as e:
                logger.error(f"Failed to initialize GLM client: {e}")
                self.client = None
        elif (provider == "gemini" or not openai_key) and gemini_key:
            self.provider = "gemini"
            self.primary_model = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
            self.fallback_model = getattr(settings, "GEMINI_MODEL_FALLBACK", "gemini-2.0-flash")
            try:
                self.client = openai.OpenAI(
                    api_key=gemini_key,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )
                logger.info(f"AI Client configured with Gemini (OpenAI-compatible) - Model: {self.primary_model}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini OpenAI-compatible client: {e}")
                self.client = None
        elif openai_key and provider == "openai":
            self.provider = "openai"
            self.primary_model = settings.OPENAI_MODEL_PRIMARY
            self.fallback_model = settings.OPENAI_MODEL_FALLBACK
            try:
                self.client = openai.OpenAI(api_key=openai_key)
                logger.info(f"AI Client configured with OpenAI - Model: {self.primary_model}")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        elif glm_key:
            self.provider = "glm"
            self.primary_model = glm_model
            self.fallback_model = glm_fallback
            try:
                self.client = openai.OpenAI(api_key=glm_key, base_url=glm_base_url)
            except Exception:
                self.client = None
        elif gemini_key:
            self.provider = "gemini"
            self.primary_model = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
            self.fallback_model = getattr(settings, "GEMINI_MODEL_FALLBACK", "gemini-2.0-flash")
            try:
                self.client = openai.OpenAI(
                    api_key=gemini_key,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )
            except Exception:
                self.client = None
        else:
            self.provider = "glm"
            self.primary_model = glm_model
            self.fallback_model = glm_fallback
            self.client = None
            logger.warning("No AI API key found (GLM_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY). AI features inactive.")

    def classify_blocks(
        self,
        text: str,
        mode: str
    ) -> Dict[str, Any]:
        """
        Semantic block classification - identifies which information blocks appear in text
        Returns: {blocks_detected: [...], confidence: 0.0-1.0, snippet: "...", page: 1}
        """
        if self.provider == "gemini" and self.native_gemini.available:
            return self.native_gemini.classify_blocks(text, mode)

        from config.information_blocks import get_information_blocks, get_block_description

        if not self.client:
            logger.warning("AI client not configured (missing GEMINI_API_KEY).")
            return {"blocks_detected": [], "confidence": 0.0, "snippet": "", "page": None}

        blocks = get_information_blocks()
        block_descriptions = []
        for block_id in blocks:
            desc = get_block_description(block_id)
            block_descriptions.append(
                f"- {block_id}: {desc.get('description', '')} "
                f"(Keywords: {', '.join(desc.get('keywords', [])[:5])})"
            )

        prompt = f"""You are a semantic information block classifier for {mode.upper()} institutional document review.

Analyze the following text chunk and identify which INFORMATION BLOCKS are present.
A single chunk may contain MULTIPLE blocks.

Available Information Blocks:
{chr(10).join(block_descriptions)}

IMPORTANT: Use SEMANTIC understanding, not just keyword matching:
- "teaching staff" or "educators" -> faculty_information
- "career outcomes" or "job placements" -> placement_information
- "built-up area" or "campus infrastructure" -> infrastructure_information
- "academic schedule" or "semester dates" -> academic_calendar_information
- "fire safety certificate" or "fire NOC" -> safety_compliance_information

Text chunk (first 3000 characters):
{text[:3000]}

Return a JSON object with:
{{
    "blocks_detected": ["block_type1", "block_type2"],
    "confidence": 0.0-1.0,
    "snippet": "relevant text snippet that supports the classification",
    "page": 1
}}

Be precise. Only include blocks that are CLEARLY present. Return empty array if none match."""

        try:
            response = safe_openai_call(
                self.client,
                self.primary_model,
                [
                    {"role": "system", "content": "You are a precise semantic classifier. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            result_text = response.choices[0].message.content
            result = parse_json_safely(result_text)

            if "blocks_detected" not in result:
                result["blocks_detected"] = []
            if "confidence" not in result:
                result["confidence"] = 0.0
            if "snippet" not in result:
                result["snippet"] = ""

            return result

        except Exception as e:
            logger.error(f"Block classification error: {e}")
            return {
                "blocks_detected": [],
                "confidence": 0.0,
                "snippet": "",
                "page": None
            }

    def extract_block_data(
        self,
        block_type: str,
        text: str,
        mode: str
    ) -> Dict[str, Any]:
        """
        Extract structured data from a specific information block
        Returns: {extracted_data: {...}, confidence: 0.0-1.0, evidence: [...]}
        """
        if self.provider == "gemini" and self.native_gemini.available:
            return self.native_gemini.extract_block_data(block_type, text, mode)

        if not self.client:
            logger.warning("AI client not configured (missing GEMINI_API_KEY).")
            return {"extracted_data": {}, "confidence": 0.0, "evidence": []}

        from config.information_blocks import get_block_fields, get_block_description

        block_desc = get_block_description(block_type)
        block_fields = get_block_fields(block_type, mode)

        required_fields = block_fields.get("required_fields", [])
        optional_fields = block_fields.get("optional_fields", [])

        schema_fields = [f"- {field}: Extract this field if mentioned" for field in required_fields + optional_fields]

        prompt = f"""You are a semantic data extraction specialist for {mode.upper()} institutional document review.

Extract structured data from this {block_type} block.

Block Description: {block_desc.get('description', '')}
Synonyms to recognize: {', '.join(block_desc.get('synonyms', []))}

Text chunk:
{text[:6000]}

Extract the following fields (use SEMANTIC understanding):
{chr(10).join(schema_fields)}

IMPORTANT: 
- Use semantic understanding: "teaching staff: 60" -> faculty_count = 60
- "educators: 60" -> faculty_count = 60
- "20 professors + 40 lecturers" -> faculty_count = 60
- Extract meaning even with synonyms or indirect phrasing
- If a field is not found, use null
- Extract ALL numeric values mentioned (counts, percentages, areas, etc.)

Return a JSON object with:
{{
    "extracted_data": {{
        "field1": value1,
        "field2": value2
    }},
    "confidence": 0.0-1.0,
    "evidence": [
        {{
            "field": "field_name",
            "value": "extracted_value",
            "page": 1,
            "snippet": "supporting text"
        }}
    ]
}}

Be precise. Always return valid JSON."""

        try:
            response = safe_openai_call(
                self.client,
                self.primary_model,
                [
                    {"role": "system", "content": "You are a precise data extractor. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            result_text = response.choices[0].message.content
            return parse_json_safely(result_text)

        except Exception as e:
            logger.error(f"Block extraction error: {e}")
            return {
                "extracted_data": {},
                "confidence": 0.0,
                "evidence": []
            }

    def chat(
        self,
        message: str,
        context: Dict[str, Any],
        mode: str
    ) -> str:
        """
        Chatbot assistant using Gemini (primary) or fallback model.
        """
        if self.provider == "gemini" and self.native_gemini.available:
            return self.native_gemini.chat(message, context, mode)

        system_prompt = context.get("system_prompt")
        if not system_prompt:
            context_str = json.dumps(context, indent=2, default=str)
            system_prompt = f"""You are a helpful assistant for {mode.upper()} reviewers analyzing institutional information blocks.

Context from the current batch:
{context_str}

Provide a clear, helpful answer based on the information blocks context.
- Explain KPIs using block data
- Explain sufficiency and compliance
- Summarize institution status based on blocks

If you don't know, say so."""

        if not self.client:
            return "AI API key is not configured. Please add GEMINI_API_KEY to your .env file."

        try:
            logger.info(f"Calling {self.primary_model} for chatbot query")
            response = safe_openai_call(
                self.client,
                self.primary_model,
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Chat error ({self.primary_model}): {e}")
            try:
                logger.info(f"Trying fallback model {self.fallback_model} for chatbot")
                response = safe_openai_call(
                    self.client,
                    self.fallback_model,
                    [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e2:
                logger.error(f"Chat error with fallback model ({self.fallback_model}): {e2}")
                return f"I apologize, but I encountered an error communicating with the AI service: {str(e2)[:100]}"
