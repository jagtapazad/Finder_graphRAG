from typing import List

from neo4j import Session

from .client import get_driver
from ..models.domain import Agent


def _session() -> Session:
    return get_driver().session()


def get_agents_by_task_type(task_type_name: str) -> List[Agent]:
    cypher = """
    MATCH (tt:TaskType {name: $taskType})-[:REQUIRES_CAPABILITY]->(cap:Capability),
          (agent:Agent)-[:HAS_CAPABILITY]->(cap)
    WITH DISTINCT agent
    RETURN agent
    """
    with _session() as session:
        result = session.run(cypher, taskType=task_type_name)
        agents: List[Agent] = []
        for record in result:
            node = record["agent"]
            agents.append(
                Agent(
                    name=node["name"],
                    capability_level=node.get("capabilityLevel", 0.5),
                    domain_expertise=node.get("domainExpertise", "general"),
                    input_format=node.get("inputFormat", "text"),
                    output_format=node.get("outputFormat", "text"),
                    historical_accuracy=node.get("historicalAccuracy", 0.5),
                )
            )
        return agents


def get_fallback_agent(agent_name: str) -> Agent | None:
    cypher = """
    MATCH (a:Agent {name: $name})-[:FALLBACK_AGENT]->(fb:Agent)
    RETURN fb LIMIT 1
    """
    with _session() as session:
        record = session.run(cypher, name=agent_name).single()
        if not record:
            return None
        node = record["fb"]
        return Agent(
            name=node["name"],
            capability_level=node.get("capabilityLevel", 0.5),
            domain_expertise=node.get("domainExpertise", "general"),
            input_format=node.get("inputFormat", "text"),
            output_format=node.get("outputFormat", "text"),
            historical_accuracy=node.get("historicalAccuracy", 0.5),
        )


def create_routing_decision(query_text: str, agent_name: str, confidence: float) -> str:
    cypher = """
    MERGE (agent:Agent {name: $agentName})
    CREATE (q:Query {text: $queryText})
    CREATE (rd:RoutingDecision {
        id: randomUUID(),
        timestamp: datetime(),
        confidence: $confidence,
        outcome: 'PENDING'
    })
    CREATE (rd)-[:SOURCE_QUERY]->(q)
    CREATE (rd)-[:ROUTED_TO]->(agent)
    RETURN rd.id AS id
    """
    with _session() as session:
        record = session.run(
            cypher,
            agentName=agent_name,
            queryText=query_text,
            confidence=confidence,
        ).single()
        return record["id"]


def update_routing_outcome(rd_id: str, outcome: str) -> None:
    cypher = """
    MATCH (rd:RoutingDecision {id: $id})
    SET rd.outcome = $outcome
    """
    with _session() as session:
        session.run(cypher, id=rd_id, outcome=outcome)


def update_agent_stats(agent_name: str, success: bool) -> None:
    cypher = """
    MATCH (a:Agent {name: $name})
    SET a.successCount = coalesce(a.successCount, 0) + CASE WHEN $success THEN 1 ELSE 0 END,
        a.failureCount = coalesce(a.failureCount, 0) + CASE WHEN $success THEN 0 ELSE 1 END,
        a.historicalAccuracy =
            toFloat(a.successCount) / (a.successCount + a.failureCount)
    """
    with _session() as session:
        session.run(cypher, name=agent_name, success=success)


