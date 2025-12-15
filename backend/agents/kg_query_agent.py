from typing import List, Tuple

from ..kg.queries import get_agents_by_task_type
from ..models.domain import Agent
from ..models.schemas import AnalyzedQuery


def score_agent(agent: Agent, analyzed: AnalyzedQuery, historical_score: float | None = None) -> tuple[float, dict]:
    hist = historical_score if historical_score is not None else agent.historical_accuracy
    
    if agent.domain_expertise == analyzed.domain:
        domain_match = 1.0
    elif agent.domain_expertise == "general":
        domain_match = 0.6
    else:
        domain_match = 0.3
    
    domain_exact_match = 1.0 if agent.domain_expertise == analyzed.domain else 0.0
    
    input_format_match = 1.0 if agent.input_format == "text" or analyzed.output_format is None else 0.8
    output_format_match = 1.0 if agent.output_format == analyzed.output_format or analyzed.output_format is None else 0.7
    
    response_time_score = 1.0 - agent.response_time if hasattr(agent, 'response_time') else 0.5
    cost_score = agent.cost_efficiency if hasattr(agent, 'cost_efficiency') else 0.5
    reliability_score = agent.reliability if hasattr(agent, 'reliability') else 0.5
    specialization_score = agent.specialization_score if hasattr(agent, 'specialization_score') else 0.5
    
    score = (
        0.25 * agent.capability_level +
        0.20 * hist +
        0.25 * domain_match +
        0.10 * response_time_score +
        0.10 * cost_score +
        0.05 * reliability_score +
        0.05 * specialization_score
    )
    
    tie_breaking = {
        "capability_level": agent.capability_level,
        "historical_accuracy": hist,
        "domain_match": domain_match,
        "domain_exact_match": domain_exact_match,
        "input_format_match": input_format_match,
        "output_format_match": output_format_match,
        "response_time_score": response_time_score,
        "cost_efficiency": cost_score,
        "reliability": reliability_score,
        "specialization_score": specialization_score,
    }
    
    return (score, tie_breaking)


def query_kg_for_agents(analyzed: AnalyzedQuery) -> List[Tuple[Agent, float, dict]]:
    """
    Query KG for agents and score them with tie-breaking information.
    Returns: List of (Agent, score, tie_breaking_info) tuples
    """
    # Pass domain to prioritize domain-specific agents in the initial query
    candidates = get_agents_by_task_type(analyzed.task_type, domain=analyzed.domain)
    scored: List[Tuple[Agent, float, dict]] = [
        (agent, score, tie_info) 
        for agent in candidates 
        for score, tie_info in [score_agent(agent, analyzed)]
    ]
    
    # Sort by score, then by tie-breaking criteria (multi-axis sorting)
    # Domain exact match is now prioritized higher to ensure domain-specific agents are preferred
    scored.sort(
        key=lambda x: (
            x[1],  # Primary: overall score
            x[2]["domain_exact_match"],  # Secondary: exact domain match (moved up from 6th)
            x[2]["capability_level"],  # Tertiary: capability level
            x[2]["historical_accuracy"],  # Quaternary: historical accuracy
            x[2]["reliability"],  # Quinary: reliability
            x[2]["specialization_score"],  # Senary: specialization
            x[2]["response_time_score"],  # Septenary: response time
            x[2]["cost_efficiency"],  # Octonary: cost efficiency
        ),
        reverse=True,
    )
    return scored


