"""
Google Gemini API Client
Primary AI Model (Gemini 1.5 Flash - Free Tier, Fast, and Cheap)
Supports both native google-generativeai SDK and OpenAI-compatible endpoint.
"""

import logging
import json
import os
import re
from typing import Dict, Any, Optional, List
from config.settings import settings
from utils.validators import parse_json_safely

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not installed. Install with: pip install google-generativeai")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class GeminiClient:
    """
    Google Gemini API client for classification, extraction, and chatbot.
    Defaults to Gemini 1.5 Flash (free tier: 15 RPM, 1M TPM, 1,500 RPD, fast).
    """

    def __init__(self):
        self.api_key = (
            settings.GEMINI_API_KEY
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or settings.UNSTRUCTURED_API_KEY
        )
        self.model_name = settings.GEMINI_MODEL or "gemini-2.5-flash"
        self.fallback_model = settings.GEMINI_MODEL_FALLBACK or "gemini-2.0-flash"
        self.client = None
        self.openai_compat_client = None
        self.available = False

        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not set. Gemini features will be inactive until configured.")
            return

        # 1. Initialize native Google Generative AI client
        if GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model_name)
                self.available = True
                logger.info(f"Gemini native client initialized with model '{self.model_name}'")
            except Exception as e:
                logger.error(f"Failed to initialize native Gemini client: {e}")

        # 2. Also initialize OpenAI-compatible client for Google Gemini
        if OPENAI_AVAILABLE:
            try:
                self.openai_compat_client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )
                self.available = True
                logger.info(f"Gemini OpenAI-compatible client initialized for model '{self.model_name}'")
            except Exception as e:
                logger.warning(f"Could not initialize Gemini OpenAI-compatible client: {e}")

    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        json_mode: bool = False,
        timeout: int = 60
    ) -> str:
        """
        Generate text completion using Gemini.
        """
        if not self.available:
            raise ValueError("Gemini client is not available (missing GEMINI_API_KEY).")

        # Try native genai first
        if self.client and GEMINI_AVAILABLE:
            try:
                generation_config = genai.types.GenerationConfig(
                    temperature=temperature,
                    response_mime_type="application/json" if json_mode else "text/plain"
                )
                
                model_to_use = self.client
                if system_prompt:
                    model_to_use = genai.GenerativeModel(
                        self.model_name,
                        system_instruction=system_prompt
                    )
                
                response = model_to_use.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                if response and hasattr(response, "text"):
                    return response.text
                elif response and hasattr(response, "parts"):
                    return "".join(part.text for part in response.parts if hasattr(part, "text"))
            except Exception as e:
                logger.warning(f"Native Gemini generate_content error: {e}. Trying OpenAI-compatible endpoint...")

        # Fallback to OpenAI-compatible endpoint
        if self.openai_compat_client:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            call_kwargs = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
                "timeout": timeout
            }
            if json_mode:
                call_kwargs["response_format"] = {"type": "json_object"}

            try:
                res = self.openai_compat_client.chat.completions.create(**call_kwargs)
                return res.choices[0].message.content
            except Exception as e:
                # Try fallback model
                logger.warning(f"OpenAI-compat call failed with {self.model_name}: {e}. Retrying with {self.fallback_model}...")
                call_kwargs["model"] = self.fallback_model
                res = self.openai_compat_client.chat.completions.create(**call_kwargs)
                return res.choices[0].message.content

        raise RuntimeError("All Gemini generation strategies failed.")

    def generate_chat_response(
        self,
        query: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.3,
        **kwargs
    ) -> Any:
        """
        Generate chatbot response using Gemini.
        Handles both:
          1) query + context + system_prompt (ChatbotService) -> returns dict
          2) messages list (GovEasyExplainer) -> returns string
        """
        if not self.available:
            raise ValueError("Gemini client is not available (missing GEMINI_API_KEY).")

        # Case 1: messages passed (e.g. GovEasyExplainer)
        if messages:
            extracted_sys = None
            extracted_user = ""
            for m in messages:
                if m.get("role") == "system":
                    extracted_sys = m.get("content")
                elif m.get("role") == "user":
                    extracted_user += ("\n" + m.get("content", ""))

            return self.generate_text(
                prompt=extracted_user.strip(),
                system_prompt=extracted_sys,
                temperature=temperature
            )

        # Case 2: standard platform query
        query_text = query or ""
        ctx = context or {}
        sys_prompt = system_prompt or "You are a helpful institutional accreditation assistant."

        prompt = f"""{sys_prompt}

CONTEXT (Platform Data Only):
{self._format_context(ctx)}

USER QUESTION: {query_text}

IMPORTANT RULES:
- Answer ONLY about the platform data provided above
- Explain scores, trends, missing documents based on real data
- NEVER hallucinate policy rules or make up data
- If data is missing, say "Not enough data" instead of fabricating
- Cite specific evidence when available

RESPONSE:"""

        answer = self.generate_text(prompt=prompt, temperature=temperature)
        citations = self._extract_citations(answer, ctx)
        related_blocks = self._extract_related_blocks(answer, ctx)

        return {
            "answer": answer,
            "citations": citations,
            "related_blocks": related_blocks,
            "requires_context": True
        }

    def classify_blocks(
        self,
        text: str,
        mode: str
    ) -> Dict[str, Any]:
        """
        Semantic block classification using Gemini.
        """
        from config.information_blocks import get_information_blocks, get_block_description

        if not self.available:
            logger.warning("Gemini client not configured (missing GEMINI_API_KEY).")
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
            raw_text = self.generate_text(
                prompt=prompt,
                system_prompt="You are a precise semantic classifier. Always return valid JSON.",
                temperature=0.1,
                json_mode=True
            )
            result = parse_json_safely(raw_text)
            if "blocks_detected" not in result:
                result["blocks_detected"] = []
            if "confidence" not in result:
                result["confidence"] = 0.0
            if "snippet" not in result:
                result["snippet"] = ""
            return result
        except Exception as e:
            logger.error(f"Gemini block classification error: {e}")
            return {"blocks_detected": [], "confidence": 0.0, "snippet": "", "page": None}

    def extract_block_data(
        self,
        block_type: str,
        text: str,
        mode: str
    ) -> Dict[str, Any]:
        """
        Extract structured data from a specific block using Gemini.
        """
        from config.information_blocks import get_block_fields, get_block_description

        if not self.available:
            return {"extracted_data": {}, "confidence": 0.0, "evidence": []}

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
            raw_text = self.generate_text(
                prompt=prompt,
                system_prompt="You are a precise data extractor. Always return valid JSON.",
                temperature=0.1,
                json_mode=True
            )
            return parse_json_safely(raw_text)
        except Exception as e:
            logger.error(f"Gemini block extraction error: {e}")
            return {"extracted_data": {}, "confidence": 0.0, "evidence": []}

    def chat(
        self,
        message: str,
        context: Dict[str, Any],
        mode: str
    ) -> str:
        """
        Chatbot assistant using Gemini.
        """
        system_prompt = context.get("system_prompt")
        if not system_prompt:
            context_str = json.dumps(context, indent=2, default=str)
            system_prompt = f"""You are a helpful assistant for {mode.upper()} reviewers analyzing institutional information blocks.

Context from the current batch:
{context_str}

Provide a clear, helpful answer based on the information blocks context.
Explain KPIs, sufficiency, and missing blocks."""

        if not self.available:
            return "Gemini API key is not configured. Please add GEMINI_API_KEY to your .env file."

        try:
            return self.generate_text(
                prompt=message,
                system_prompt=system_prompt,
                temperature=0.7
            )
        except Exception as e:
            logger.error(f"Gemini chat error: {e}")
            return f"I apologize, but I encountered an error communicating with Gemini: {str(e)[:120]}"

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context for prompt"""
        parts = []

        if context.get("kpi_results"):
            parts.append("KPIs:")
            for kpi_id, kpi_data in context["kpi_results"].items():
                if isinstance(kpi_data, dict) and kpi_data.get("value") is not None:
                    parts.append(f"  - {kpi_data.get('name', kpi_id)}: {kpi_data.get('value')}")

        if context.get("sufficiency_result"):
            sufficiency = context["sufficiency_result"]
            parts.append(f"Document Sufficiency: {sufficiency.get('percentage', 0)}%")

        if context.get("compliance_results"):
            parts.append(f"Compliance Flags: {len(context['compliance_results'])} issues found")

        if context.get("block_summaries"):
            parts.append("Available Data Blocks:")
            for block_type, summary in context["block_summaries"].items():
                if summary.get("present"):
                    parts.append(f"  - {block_type}: {summary.get('fields_count', 0)} fields extracted")

        return "\n".join(parts) if parts else "No context data available"

    def _extract_citations(self, answer: str, context: Dict[str, Any]) -> List[str]:
        """Extract citation references from answer"""
        citations = []
        if context.get("block_summaries"):
            for block_type in context["block_summaries"].keys():
                if block_type.lower() in answer.lower():
                    citations.append(f"Data from {block_type} block")
        return citations

    def _extract_related_blocks(self, answer: str, context: Dict[str, Any]) -> List[str]:
        """Extract related block types mentioned in answer"""
        related = []
        if context.get("block_summaries"):
            for block_type in context["block_summaries"].keys():
                if block_type.lower() in answer.lower():
                    related.append(block_type)
        return related
