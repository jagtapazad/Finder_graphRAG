from crewai import Crew

from .agents import (
    code_analysis_agent,
    extractor_agent,
    fallback_agent,
    feedback_agent,
    kg_query_agent,
    router_agent,
    summarization_agent,
    web_search_agent,
)
from ..agents.kg_query_agent import query_kg_for_agents
from ..config import settings
from ..extraction.llm_extractor import extract_query
from ..kg.queries import create_routing_decision, get_fallback_agent

router_crew = Crew(
    name="SmartAgenticRouterCrew",
    agents=[
        extractor_agent,
        kg_query_agent,
        router_agent,
        web_search_agent,
        code_analysis_agent,
        summarization_agent,
        fallback_agent,
        feedback_agent,
    ],
)


def run_routing_flow(user_query: str) -> dict:
    # Step 1: Extraction (LLM)
    analyzed = extract_query(user_query)

    # Step 2: KG query
    ranked = query_kg_for_agents(analyzed)

    # Step 3: Routing decision
    if not ranked:
        chosen_name = "PerplexityFallbackAgent"
        confidence = 0.5
        candidates: list[dict] = []
    else:
        top_agent, top_score = ranked[0]
        chosen_name = top_agent.name
        confidence = top_score

        if confidence < settings.low_conf_threshold:
            fb = get_fallback_agent(chosen_name)
            if fb:
                chosen_name = fb.name

        candidates = [
            {"name": agent.name, "score": score}
            for agent, score in ranked[:3]
        ]

    rd_id = create_routing_decision(user_query, chosen_name, confidence)

    # Step 4: Execution step (call appropriate LLM/tool based on chosen_name)
    # For now, this is a stub. You can branch on chosen_name to call
    # web search, code analysis, summarization, etc.

    result_payload = {
        "routing_decision_id": rd_id,
        "chosen_agent": chosen_name,
        "confidence": confidence,
        "analyzed_query": analyzed,
        "top_candidates": candidates,
    }
    return result_payload


