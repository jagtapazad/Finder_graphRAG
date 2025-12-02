import json
from typing import Any

import google.generativeai as genai

from ..config import settings
from ..models.schemas import AnalyzedQuery
from .prompt_templates import EXTRACTION_PROMPT_TEMPLATE


class ExtractionError(Exception):
    pass


def call_llm(prompt: str) -> str:
    """
    Calls Google Gemini LLM for query extraction.
    """
    if not settings.llm_api_key:
        # Fallback to simple heuristic JSON if no API key is set.
        # This makes local dev easier before wiring a real model.
        fallback = {
            "task_type": "WebSearchTask",
            "complexity": 0.5,
            "domain": "general",
            "output_format": None,
            "free_text": prompt,
        }
        return json.dumps(fallback)

    # Configure Gemini with API key
    genai.configure(api_key=settings.llm_api_key)
    
    # Create model instance
    model = genai.GenerativeModel(settings.llm_model)
    
    # Build the full prompt with system instruction
    full_prompt = f"You are a JSON-only task extraction model. {prompt}"
    
    try:
        # Generate response
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # Lower temperature for more consistent JSON output
                max_output_tokens=500,
            ),
        )
        
        # Extract text from response
        if response.text:
            return response.text.strip()
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


