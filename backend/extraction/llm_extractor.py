import json
from typing import Any

import google.generativeai as genai

from ..config import settings
from ..models.schemas import AnalyzedQuery
from .prompt_templates import EXTRACTION_PROMPT_TEMPLATE


class ExtractionError(Exception):
    pass


def call_llm(prompt: str) -> str:
    if not settings.llm_api_key:
        fallback = {
            "task_type": "WebSearchTask",
            "complexity": 0.5,
            "domain": "general",
            "output_format": None,
            "free_text": prompt,
        }
        return json.dumps(fallback)

    genai.configure(api_key=settings.llm_api_key)
    
    model_name = settings.llm_model.replace("gemini/", "") if settings.llm_model.startswith("gemini/") else settings.llm_model
    if not model_name.startswith("models/"):
        model_name = f"models/{model_name}"
    model = genai.GenerativeModel(model_name)
    
    full_prompt = f"You are a JSON-only task extraction model. {prompt}"
    
    try:
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=500,
                response_mime_type="application/json",
            ),
        )
        
        if response.text:
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return text.strip()
        else:
            raise ExtractionError("Empty response from Gemini")
            
    except Exception as e:
        raise ExtractionError(f"Gemini API error: {e}") from e


def extract_query(query_text: str) -> AnalyzedQuery:
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(query=query_text)
    raw_response = call_llm(prompt)

    try:
        data: dict[str, Any] = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ExtractionError(f"Invalid JSON from LLM: {exc}") from exc

    return AnalyzedQuery(
        raw_text=query_text,
        task_type=data.get("task_type", "WebSearchTask"),
        complexity=float(data.get("complexity", 0.5)),
        domain=data.get("domain", "general"),
        output_format=data.get("output_format"),
    )


