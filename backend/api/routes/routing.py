from fastapi import APIRouter

from ...crew.crew_config import run_routing_flow
from ...models.schemas import RouteRequest, RoutingResult

router = APIRouter()


@router.post("/", response_model=RoutingResult)
def route(route_request: RouteRequest) -> RoutingResult:
    result = run_routing_flow(route_request.query)
    return RoutingResult(
        routing_decision_id=result["routing_decision_id"],
        chosen_agent=result["chosen_agent"],
        confidence=result["confidence"],
        rationale={
            "analyzed_query": result["analyzed_query"].dict(),
            "top_candidates": result["top_candidates"],
        },
    )


