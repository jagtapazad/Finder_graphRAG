from ..kg.queries import update_agent_stats, update_routing_outcome


def record_feedback(routing_decision_id: str, agent_name: str, success: bool) -> None:
    outcome = "SUCCESS" if success else "FAILURE"
    update_routing_outcome(routing_decision_id, outcome)
    update_agent_stats(agent_name, success)


