from fastapi import APIRouter

from ...kg.queries import get_routing_metrics

router = APIRouter()


@router.get("/")
def get_routing_metrics_endpoint():
    """
    Returns routing metrics for dashboard display.
    
    Returns:
    - total_decisions: Total number of routing decisions made
    - average_confidence: Average confidence score across all decisions
    - agent_performance: List of agents with success rates
    - recent_accuracy_trend: Daily accuracy trends over last 30 days
    
    Example response:
    {
        "total_decisions": 150,
        "average_confidence": 0.82,
        "agent_performance": [
            {
                "agent_name": "WebSearchAgent",
                "total": 50,
                "successes": 45,
                "failures": 5,
                "success_rate": 0.9
            },
            ...
        ],
        "recent_accuracy_trend": [
            {
                "day": "2025-01-15",
                "total": 10,
                "successes": 9,
                "accuracy": 0.9
            },
            ...
        ]
    }
    """
    try:
        return get_routing_metrics()
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching metrics: {str(e)}",
        )

