from fastapi import APIRouter, HTTPException
import traceback

from ...crew.crew_config import run_routing_flow
from ...models.schemas import RouteRequest, RoutingResult

router = APIRouter()


@router.post("/", response_model=RoutingResult)
def route(route_request: RouteRequest) -> RoutingResult:
    try:
        result = run_routing_flow(route_request.query)
        analyzed = result["analyzed_query"]
        return RoutingResult(
            routing_decision_id=result["routing_decision_id"],
            chosen_agent=result["chosen_agent"],
            confidence=result["confidence"],
            rationale={
                "analyzed_query": analyzed.dict(),
                "top_candidates": result["top_candidates"],
                "task_type": analyzed.task_type,
                "tie_breaking_info": result.get("tie_breaking_info", {}),
            },
        )
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error in routing endpoint: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


