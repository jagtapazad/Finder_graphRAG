from typing import List, Tuple

from ..kg.queries import get_agents_by_task_type
from ..models.domain import Agent
from ..models.schemas import AnalyzedQuery


def score_agent(agent: Agent, analyzed: AnalyzedQuery, historical_score: float | None = None) -> float:
    """
    Simple scoring that combines capability level, historical accuracy, and domain match.
    """
    hist = historical_score if historical_score is not None else agent.historical_accuracy
    domain_match = 1.0 if agent.domain_expertise in (analyzed.domain, "general") else 0.7
    return 0.5 * agent.capability_level + 0.3 * hist + 0.2 * domain_match


def query_kg_for_agents(analyzed: AnalyzedQuery) -> List[Tuple[Agent, float]]:
    candidates = get_agents_by_task_type(analyzed.task_type)
    scored: List[Tuple[Agent, float]] = [(agent, score_agent(agent, analyzed)) for agent in candidates]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


