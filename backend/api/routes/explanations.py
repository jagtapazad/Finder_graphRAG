from fastapi import APIRouter, HTTPException

from ...kg.queries import get_routing_explanation, get_routing_path
from ...models.schemas import AnalyzedQuery

router = APIRouter()


@router.get("/routing/{routing_decision_id}/explanation")
def get_routing_explanation_endpoint(routing_decision_id: str, task_type: str):
    """
    Returns the graph traversal path explaining WHY an agent was chosen.
    
    Shows the complete path:
    Query -> TaskType -> Required Capabilities -> Agent Capabilities -> Selected Agent
    
    This demonstrates explainable routing by walking the knowledge graph.
    """
    try:
        explanation = get_routing_explanation(routing_decision_id, task_type)
        if not explanation:
            raise HTTPException(
                status_code=404,
                detail=f"Routing decision {routing_decision_id} not found or invalid task_type {task_type}",
            )
        return explanation
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching explanation: {str(e)}",
        )


@router.get("/routing/{routing_decision_id}/path")
def get_routing_path_endpoint(routing_decision_id: str, task_type: str):
    """
    Returns the full graph traversal path for visualization.
    
    This endpoint provides the complete routing path including:
    - Query text
    - Task type
    - Required capabilities
    - Selected agent
    - Agent capabilities
    - Matching capabilities (intersection)
    """
    path = get_routing_path(routing_decision_id, task_type)
    if not path:
        raise HTTPException(
            status_code=404,
            detail=f"Routing decision {routing_decision_id} not found or invalid task_type {task_type}",
        )
    return path

