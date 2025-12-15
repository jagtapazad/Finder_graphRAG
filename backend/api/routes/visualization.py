from fastapi import APIRouter

from ...kg.queries import get_kg_for_visualization

router = APIRouter()


@router.get("/kg/visualization")
def get_kg_visualization():
    """
    Returns graph data in format suitable for visualization (e.g., vis.js, D3.js, react-force-graph).
    
    Returns:
    - nodes: List of nodes (agents, capabilities, task types) with properties
    - edges: List of edges (relationships) connecting nodes
    
    Node format:
    {
        "id": "node_id",
        "label": "Node Name",
        "type": "Agent|Capability|TaskType|Query|RoutingDecision",
        "properties": {...}
    }
    
    Edge format:
    {
        "id": "edge_id",
        "source": "source_node_id",
        "target": "target_node_id",
        "type": "HAS_CAPABILITY|REQUIRES_CAPABILITY|ROUTED_TO|...",
        "properties": {...}
    }
    """
    try:
        return get_kg_for_visualization()
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching visualization data: {str(e)}",
        )

