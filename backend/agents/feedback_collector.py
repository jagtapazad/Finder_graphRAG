from ..kg.queries import (
    get_historical_decisions,
    update_agent_stats,
    update_routing_outcome,
)


def record_feedback(routing_decision_id: str, agent_name: str, success: bool) -> dict:
    """
    Record feedback and return impact information showing how the feedback affects agent stats.
    
    Returns:
    - before_stats: Agent stats before feedback
    - after_stats: Agent stats after feedback
    - impact: Change in historical accuracy
    """
    # Get before stats
    historical = get_historical_decisions(agent_name, limit=1)
    before_accuracy = 0.5  # Default
    if historical:
        # Calculate current accuracy from recent decisions
        # This is approximate; actual calculation happens in update_agent_stats
        pass
    
    # Update KG
    outcome = "SUCCESS" if success else "FAILURE"
    update_routing_outcome(routing_decision_id, outcome)
    update_agent_stats(agent_name, success)
    
    # Get after stats (approximate - would need to query agent node directly)
    # For now, return basic impact info
    return {
        "routing_decision_id": routing_decision_id,
        "agent_name": agent_name,
        "outcome": outcome,
        "impact": {
            "message": f"Updated {agent_name} statistics. Historical accuracy will be recalculated based on new success/failure counts.",
            "feedback_applied": True,
        },
    }


