EXTRACTION_PROMPT_TEMPLATE = """
You are a task understanding assistant. Given a user query, output JSON with:
- task_type: one of ["WebSearchTask", "CodeDebuggingTask", "SummarizationTask", "VisualizationTask", "OtherTask"]
- complexity: float between 0.0 and 1.0
- domain: one of ["technical", "general", "legal", "medical", "research", "finance", "education", "content", "analytics", "development", "security", "automation", "media"] - choose the most specific domain that matches the query content
- output_format: string or null
- free_text: the original user query

Important domain classification rules:
- For queries mentioning "medical", "biomedical", "health", "clinical", "patient", "disease", "treatment", "diagnosis", etc., use domain: "medical"
- For queries mentioning "research", "academic", "papers", "studies", "literature", "publication", etc., use domain: "research"
- For queries mentioning "code", "programming", "software", "debug", "algorithm", etc., use domain: "technical" or "development"
- For queries mentioning "legal", "law", "contract", "compliance", "regulation", etc., use domain: "legal"
- For queries mentioning "financial", "investment", "stock", "market", "trading", etc., use domain: "finance"
- If no specific domain matches, use domain: "general"

Respond with ONLY JSON, no extra text.

User query: "{query}"
"""


