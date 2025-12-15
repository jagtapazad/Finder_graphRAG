from fastapi import APIRouter, HTTPException

from ...agents.feedback_collector import record_feedback
from ...kg.queries import _session  # type: ignore[attr-defined]
from ...models.schemas import FeedbackRequest

router = APIRouter()


def _get_agent_name_for_routing_decision(routing_decision_id: str) -> str | None:
    cypher = """
    MATCH (rd:RoutingDecision {id: $id})-[:ROUTED_TO]->(a:Agent)
    RETURN a.name AS name
    """
    with _session() as session:  # reuse the same helper as other KG queries
        record = session.run(cypher, id=routing_decision_id).single()
        if not record:
            return None
        return record["name"]


@router.post("/")
def submit_feedback(feedback: FeedbackRequest) -> dict:
    """
    Submit feedback for a routing decision.
    Returns impact information showing how feedback affects agent performance.
    """
    try:
        agent_name = _get_agent_name_for_routing_decision(feedback.routing_decision_id)
        if not agent_name:
            raise HTTPException(status_code=404, detail="RoutingDecision not found")

        impact = record_feedback(feedback.routing_decision_id, agent_name, feedback.success)
        return {
            "status": "ok",
            "routing_decision_id": feedback.routing_decision_id,
            "agent_name": agent_name,
            "feedback_applied": True,
            "impact": impact.get("impact", {}),
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in feedback endpoint: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


