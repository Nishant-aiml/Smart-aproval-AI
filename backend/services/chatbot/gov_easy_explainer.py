"""
GovEasy Explainer
Explains government documents in simple language using Gemini API (Gemini 1.5 Flash)
"""

import logging
from typing import Dict, Any, Optional
from ai.gemini_client import GeminiClient
from ai.openai_utils import safe_openai_call
from config.settings import settings

logger = logging.getLogger(__name__)


class GovEasyExplainer:
    """
    Explains government documents (circulars, letters, schemes) in simple language.
    Uses Gemini API (Gemini 1.5 Flash) as primary engine.
    """
    
    def __init__(self):
        self.gemini_client = GeminiClient()
    
    def explain_document(
        self,
        extracted_text: str,
        document_type: str,
        user_question: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Explain government document in simple language.
        """
        if not extracted_text or len(extracted_text.strip()) < 50:
            return {
                "explanation": "I could not extract sufficient text from this document. Please ensure the document is clear and readable.",
                "who_applies": None,
                "deadlines": [],
                "benefits": [],
                "required_documents": [],
                "consequences": [],
                "next_steps": [],
                "citations": [],
                "error": "Insufficient text extracted"
            }
        
        # Build prompt for Gemini
        prompt = self._build_explanation_prompt(extracted_text, document_type, user_question)
        
        # 1. Try Gemini primary (Gemini 1.5 Flash)
        try:
            if self.gemini_client.available:
                logger.info(f"Using Gemini ({self.gemini_client.model_name}) for GovEasy explanation")
                raw_response = self.gemini_client.generate_text(
                    prompt=prompt,
                    temperature=0.2,
                    json_mode=True
                )
                
                if raw_response:
                    result = self._parse_explanation_response(raw_response, extracted_text)
                    result["model_used"] = self.gemini_client.model_name
                    return result
        except Exception as e:
            logger.warning(f"Gemini API failed for GovEasy: {e}, trying fallback")
        
        # 2. Try Fallback via OpenAI-compatible endpoint or fallback model
        try:
            logger.info("Using fallback for GovEasy explanation")
            from ai.openai_client import OpenAIClient
            ai_client = OpenAIClient()
            if ai_client.client:
                response = safe_openai_call(
                    ai_client.client,
                    model=ai_client.primary_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                if response and hasattr(response, "choices") and response.choices:
                    raw_content = response.choices[0].message.content
                    result = self._parse_explanation_response(raw_content, extracted_text)
                    result["model_used"] = ai_client.primary_model
                    result["fallback_used"] = True
                    return result
        except Exception as e:
            logger.error(f"GovEasy fallback also failed: {e}")
        
        # If all fail, return clean error message
        return {
            "explanation": "I apologize, but I encountered an error while explaining this document. Please ensure your GEMINI_API_KEY is configured in your .env file.",
            "who_applies": None,
            "deadlines": [],
            "benefits": [],
            "required_documents": [],
            "consequences": [],
            "next_steps": [],
            "citations": [],
            "error": "Gemini explanation unavailable"
        }
    
    def _build_explanation_prompt(
        self,
        extracted_text: str,
        document_type: str,
        user_question: Optional[str]
    ) -> str:
        """Build prompt for document explanation."""
        base_prompt = f"""You are a helpful assistant that explains government documents in simple, clear language.

Document Type: {document_type.upper()}

Document Text:
{extracted_text[:12000]}

"""
        if user_question:
            base_prompt += f"""User Question: {user_question}

"""
        base_prompt += """Please provide a structured explanation in JSON format with the following fields:

{
  "explanation": "Simple, clear explanation of what this document means in plain English (2-3 paragraphs)",
  "who_applies": "Who this document applies to (e.g., 'All engineering colleges', 'New universities only', etc.)",
  "deadlines": ["List of important deadlines mentioned in the document"],
  "benefits": ["List of benefits, features, or advantages mentioned"],
  "required_documents": ["List of documents or information required"],
  "consequences": ["What happens if deadlines are missed or requirements not met"],
  "next_steps": ["Action items checklist for the user"],
  "citations": ["Page numbers or section references where key information was found"]
}

IMPORTANT RULES:
1. ONLY use information from the document text provided above
2. Do NOT add information not present in the document
3. If information is missing, say "Not mentioned in document"
4. Use simple, clear language - avoid legal jargon
5. Be specific about dates, deadlines, and requirements
6. If user asked a specific question, focus your explanation on answering that question

Return ONLY valid JSON, no additional text.
"""
        return base_prompt
    
    def _parse_explanation_response(
        self,
        response: str,
        extracted_text: str
    ) -> Dict[str, Any]:
        """Parse LLM response into structured format."""
        import json
        import re
        
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                
                result = {
                    "explanation": parsed.get("explanation", "Could not generate explanation."),
                    "who_applies": parsed.get("who_applies"),
                    "deadlines": parsed.get("deadlines", []),
                    "benefits": parsed.get("benefits", []),
                    "required_documents": parsed.get("required_documents", []),
                    "consequences": parsed.get("consequences", []),
                    "next_steps": parsed.get("next_steps", []),
                    "citations": parsed.get("citations", [])
                }
                
                for key in ["deadlines", "benefits", "required_documents", "consequences", "next_steps", "citations"]:
                    if not isinstance(result[key], list):
                        result[key] = [result[key]] if result[key] else []
                
                return result
        except Exception as e:
            logger.warning(f"Failed to parse JSON response: {e}, using fallback")
        
        return {
            "explanation": str(response)[:1000],
            "who_applies": None,
            "deadlines": [],
            "benefits": [],
            "required_documents": [],
            "consequences": [],
            "next_steps": [],
            "citations": []
        }
