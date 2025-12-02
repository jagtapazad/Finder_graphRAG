from pydantic import BaseModel


class RouteRequest(BaseModel):
    query: str


class AnalyzedQuery(BaseModel):
    raw_text: str
    task_type: str
    complexity: float
    domain: str
    output_format: str | None = None


class RoutingResult(BaseModel):
    routing_decision_id: str
    chosen_agent: str
    confidence: float
    rationale: dict


class FeedbackRequest(BaseModel):
    routing_decision_id: str
    success: bool


