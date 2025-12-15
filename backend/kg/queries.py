from typing import List, Dict, Any, Optional

from neo4j import Session

from .client import get_driver
from .key_queries import (
    QUERY_1_FIND_AGENTS_BY_TASK,
    QUERY_2_FIND_SIMILAR_AGENTS,
    QUERY_3_HISTORICAL_DECISIONS,
    QUERY_4_AGENTS_BY_DOMAIN,
    QUERY_5_ROUTING_EXPLANATION,
    QUERY_6_ROUTING_PATH,
)
from ..models.domain import Agent


def _session() -> Session:
    return get_driver().session()


def get_agents_by_task_type(task_type_name: str, min_threshold: float = 0.0, domain: str | None = None) -> List[Agent]:
    def _create_agent_from_node(node) -> Agent:
        return Agent(
            name=node["name"],
            capability_level=node.get("capabilityLevel", 0.5),
            domain_expertise=node.get("domainExpertise", "general"),
            input_format=node.get("inputFormat", "text"),
            output_format=node.get("outputFormat", "text"),
            historical_accuracy=node.get("historicalAccuracy", 0.5),
            response_time=node.get("responseTime", 1.0),
            cost_efficiency=node.get("costEfficiency", 0.5),
            reliability=node.get("reliability", 0.5),
            specialization_score=node.get("specializationScore", 0.5),
            description=node.get("description", ""),
        )
    
    if domain:
        cypher = """
        MATCH (tt:TaskType {name: $taskType})-[:REQUIRES_CAPABILITY]->(cap:Capability),
              (agent:Agent)-[:HAS_CAPABILITY]->(cap)
        WITH DISTINCT agent, agent.capabilityLevel AS capLevel,
             CASE WHEN agent.domainExpertise = $domain THEN 1 ELSE 0 END AS domainPriority
        WHERE capLevel >= $minThreshold
        RETURN agent, capLevel, agent.historicalAccuracy AS histAcc, agent.domainExpertise AS domain
        ORDER BY domainPriority DESC, capLevel DESC, histAcc DESC
        """
        with _session() as session:
            result = session.run(
                cypher,
                taskType=task_type_name,
                minThreshold=min_threshold,
                domain=domain,
            )
            agents: List[Agent] = []
            for record in result:
                agents.append(_create_agent_from_node(record["agent"]))
            
            if agents:
                return agents
    else:
        with _session() as session:
            result = session.run(
                QUERY_1_FIND_AGENTS_BY_TASK,
                taskType=task_type_name,
                minThreshold=min_threshold,
            )
            agents: List[Agent] = []
            for record in result:
                agents.append(_create_agent_from_node(record["agent"]))
            
            if agents:
                return agents
    
    fallback_cypher = """
    MATCH (agent:Agent)
    WHERE agent.capabilityLevel >= $minThreshold
    OPTIONAL MATCH (agent)-[:HAS_CAPABILITY]->(cap:Capability)
    WITH agent, agent.capabilityLevel AS capLevel,
         collect(DISTINCT cap.name) AS capabilities,
         CASE WHEN agent.domainExpertise = $domain THEN 1 ELSE 0 END AS domainPriority
    WHERE $domain IS NULL OR agent.domainExpertise = $domain OR agent.domainExpertise = 'general'
    RETURN agent, capLevel, agent.historicalAccuracy AS histAcc, agent.domainExpertise AS domain, capabilities
    ORDER BY domainPriority DESC, capLevel DESC, histAcc DESC
    """
    
    with _session() as session:
        result = session.run(
            fallback_cypher,
            minThreshold=min_threshold,
            domain=domain,
        )
        agents: List[Agent] = []
        for record in result:
            agents.append(_create_agent_from_node(record["agent"]))
        
        if not agents:
            all_agents_cypher = """
            MATCH (agent:Agent)
            RETURN agent, 
                   agent.capabilityLevel AS capLevel, 
                   agent.historicalAccuracy AS histAcc, 
                   agent.domainExpertise AS domain
            ORDER BY capLevel DESC, histAcc DESC
            """
            result = session.run(all_agents_cypher)
            for record in result:
                agents.append(_create_agent_from_node(record["agent"]))
        
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
    # First update the counts
    cypher_update_counts = """
    MATCH (a:Agent {name: $name})
    SET a.successCount = coalesce(a.successCount, 0) + CASE WHEN $success THEN 1 ELSE 0 END,
        a.failureCount = coalesce(a.failureCount, 0) + CASE WHEN $success THEN 0 ELSE 1 END
    """
    # Then calculate accuracy based on updated counts
    cypher_update_accuracy = """
    MATCH (a:Agent {name: $name})
    WITH a, coalesce(a.successCount, 0) AS successCount, coalesce(a.failureCount, 0) AS failureCount
    SET a.historicalAccuracy =
        CASE 
            WHEN (successCount + failureCount) > 0 
            THEN toFloat(successCount) / (successCount + failureCount)
            ELSE 0.5
        END
    """
    with _session() as session:
        session.run(cypher_update_counts, name=agent_name, success=success)
        session.run(cypher_update_accuracy, name=agent_name)


def get_similar_agents(agent_name: str) -> List[Agent]:
    """
    Find similar agents based on shared capabilities.
    Uses Query 2 from key_queries.py
    """
    with _session() as session:
        result = session.run(QUERY_2_FIND_SIMILAR_AGENTS, agentName=agent_name)
        agents: List[Agent] = []
        for record in result:
            node = record["a2"]
            agents.append(
                Agent(
                    name=node["name"],
                    capability_level=node.get("capabilityLevel", 0.5),
                    domain_expertise=node.get("domainExpertise", "general"),
                    input_format=node.get("inputFormat", "text"),
                    output_format=node.get("outputFormat", "text"),
                    historical_accuracy=node.get("historicalAccuracy", 0.5),
                    response_time=node.get("responseTime", 1.0),
                    cost_efficiency=node.get("costEfficiency", 0.5),
                    reliability=node.get("reliability", 0.5),
                    specialization_score=node.get("specializationScore", 0.5),
                    description=node.get("description", ""),
                )
            )
        return agents


def get_historical_decisions(agent_name: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Retrieve historical routing decisions for an agent.
    Uses Query 3 from key_queries.py
    """
    with _session() as session:
        result = session.run(QUERY_3_HISTORICAL_DECISIONS, agentName=agent_name)
        decisions = []
        for record in result:
            query_node = record.get("query")
            query_text = None
            if query_node:
                # Handle Neo4j node object - access properties like a dict
                query_text = query_node.get("text") if hasattr(query_node, "get") else (query_node["text"] if isinstance(query_node, dict) else None)
            decisions.append({
                "decision_id": record["decisionId"],
                "confidence": record["confidence"],
                "outcome": record["outcome"],
                "timestamp": record["timestamp"],
                "query_text": query_text,
            })
        return decisions[:limit]


def get_agents_by_domain(domain: str) -> List[Agent]:
    """
    Find agents by domain expertise.
    Uses Query 4 from key_queries.py
    """
    with _session() as session:
        result = session.run(QUERY_4_AGENTS_BY_DOMAIN, domain=domain)
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
                    response_time=node.get("responseTime", 1.0),
                    cost_efficiency=node.get("costEfficiency", 0.5),
                    reliability=node.get("reliability", 0.5),
                    specialization_score=node.get("specializationScore", 0.5),
                    description=node.get("description", ""),
                )
            )
        return agents


def get_routing_explanation(rd_id: str, task_type: str) -> Optional[Dict[str, Any]]:
    """
    Get the complete routing explanation showing why an agent was chosen.
    Uses Query 5 from key_queries.py
    """
    with _session() as session:
        result = session.run(
            QUERY_5_ROUTING_EXPLANATION,
            rdId=rd_id,
            taskType=task_type,
        )
        record = result.single()
        if not record:
            return None
        
        return {
            "agent_name": record["agentName"],
            "capability_level": record["capabilityLevel"],
            "historical_accuracy": record["historicalAccuracy"],
            "domain_expertise": record["domainExpertise"],
            "query_text": record["queryText"],
            "confidence": record["confidence"],
            "all_capabilities": record["allCapabilities"],
            "matching_capabilities": record["matchingCapabilities"],
            "matching_capability_count": record["matchingCapabilityCount"],
        }


def get_routing_path(rd_id: str, task_type: str) -> Optional[Dict[str, Any]]:
    """
    Get the full graph traversal path for visualization.
    Uses Query 6 from key_queries.py
    """
    with _session() as session:
        result = session.run(
            QUERY_6_ROUTING_PATH,
            rdId=rd_id,
            taskType=task_type,
        )
        record = result.single()
        if not record:
            return None
        
        return {
            "query_text": record["queryText"],
            "task_type": record["taskType"],
            "required_capabilities": record["requiredCapabilities"],
            "selected_agent": record["selectedAgent"],
            "agent_capabilities": record["agentCapabilities"],
            "matching_capabilities": record["matchingCapabilities"],
        }


def get_kg_for_visualization() -> Dict[str, Any]:
    """
    Get the complete knowledge graph structure for visualization.
    Returns nodes and edges in a format suitable for graph visualization libraries.
    """
    # First, get all nodes
    nodes_cypher = """
    MATCH (n)
    RETURN n
    """
    
    # Then, get all relationships
    edges_cypher = """
    MATCH (a)-[r]->(b)
    RETURN a, r, b
    """
    
    with _session() as session:
        nodes = []
        edges = []
        node_ids = set()
        
        # Get all nodes
        try:
            nodes_result = session.run(nodes_cypher)
            for record in nodes_result:
                node = record["n"]
                node_id = str(node.id)
                if node_id not in node_ids:
                    node_ids.add(node_id)
                    # Get node label (name property or first label)
                    node_name = node.get("name")
                    if not node_name and node.labels:
                        node_name = list(node.labels)[0]
                    if not node_name:
                        node_name = "Unknown"
                    
                    node_data = {
                        "id": node_id,
                        "label": str(node_name),
                        "type": list(node.labels)[0] if node.labels else "Unknown",
                        "properties": dict(node),
                    }
                    nodes.append(node_data)
        except Exception as e:
            print(f"Error fetching nodes: {e}")
            return {"nodes": [], "edges": [], "error": str(e)}
        
        # Get all edges
        try:
            edges_result = session.run(edges_cypher)
            edge_count = 0
            for record in edges_result:
                edge = record["r"]
                source_node = record["a"]
                target_node = record["b"]
                
                if edge and source_node and target_node:
                    try:
                        source_id = str(source_node.id)
                        target_id = str(target_node.id)
                        
                        # Verify both nodes exist in our nodes list
                        source_exists = any(n["id"] == source_id for n in nodes)
                        target_exists = any(n["id"] == target_id for n in nodes)
                        
                        if not source_exists:
                            print(f"Warning: Edge source node {source_id} not in nodes list")
                        if not target_exists:
                            print(f"Warning: Edge target node {target_id} not in nodes list")
                        
                        edge_data = {
                            "id": str(edge.id),
                            "source": source_id,
                            "target": target_id,
                            "type": edge.type,
                            "properties": {},
                        }
                        # Try to get edge properties if they exist
                        try:
                            edge_data["properties"] = dict(edge)
                        except:
                            pass
                        edges.append(edge_data)
                        edge_count += 1
                    except Exception as e:
                        # Skip edges that can't be processed
                        print(f"Error processing edge: {e}")
                        import traceback
                        traceback.print_exc()
                        continue
            
            print(f"Successfully fetched {edge_count} edges out of {len(edges)} processed")
        except Exception as e:
            print(f"Error fetching edges: {e}")
            import traceback
            traceback.print_exc()
            # Return nodes even if edges fail
            return {"nodes": nodes, "edges": [], "error": f"Error fetching edges: {str(e)}"}
        
        print(f"Returning {len(nodes)} nodes and {len(edges)} edges")
        return {"nodes": nodes, "edges": edges}


def get_routing_metrics() -> Dict[str, Any]:
    """
    Get routing metrics for dashboard display.
    """
    cypher_total = """
    MATCH (rd:RoutingDecision)
    RETURN count(rd) AS total_decisions
    """
    
    cypher_avg_confidence = """
    MATCH (rd:RoutingDecision)
    WHERE rd.confidence IS NOT NULL
    RETURN avg(rd.confidence) AS avg_confidence
    """
    
    cypher_by_agent = """
    MATCH (rd:RoutingDecision)-[:ROUTED_TO]->(agent:Agent)
    WHERE rd.outcome IS NOT NULL AND rd.outcome <> 'PENDING'
    WITH agent, rd.outcome AS outcome
    RETURN agent.name AS agent_name,
           count(*) AS total,
           sum(CASE WHEN outcome = 'SUCCESS' THEN 1 ELSE 0 END) AS successes,
           sum(CASE WHEN outcome = 'FAILURE' THEN 1 ELSE 0 END) AS failures,
           toFloat(sum(CASE WHEN outcome = 'SUCCESS' THEN 1 ELSE 0 END)) / count(*) AS success_rate
    ORDER BY total DESC
    """
    
    cypher_recent_accuracy = """
    MATCH (rd:RoutingDecision)
    WHERE rd.outcome IS NOT NULL AND rd.outcome <> 'PENDING'
      AND rd.timestamp > datetime() - duration({days: 30})
    WITH date(rd.timestamp) AS day, rd.outcome AS outcome
    RETURN day,
           count(*) AS total,
           sum(CASE WHEN outcome = 'SUCCESS' THEN 1 ELSE 0 END) AS successes
    ORDER BY day DESC
    LIMIT 30
    """
    
    with _session() as session:
        total_result = session.run(cypher_total).single()
        avg_conf_result = session.run(cypher_avg_confidence).single()
        agent_result = session.run(cypher_by_agent)
        recent_result = session.run(cypher_recent_accuracy)
        
        total_decisions = total_result["total_decisions"] if total_result else 0
        avg_confidence = float(avg_conf_result["avg_confidence"]) if avg_conf_result and avg_conf_result["avg_confidence"] else 0.0
        
        agent_stats = []
        for record in agent_result:
            agent_stats.append({
                "agent_name": record["agent_name"],
                "total": record["total"],
                "successes": record["successes"],
                "failures": record["failures"],
                "success_rate": float(record["success_rate"]) if record["success_rate"] else 0.0,
            })
        
        recent_accuracy = []
        for record in recent_result:
            recent_accuracy.append({
                "day": str(record["day"]),
                "total": record["total"],
                "successes": record["successes"],
                "accuracy": float(record["successes"]) / record["total"] if record["total"] > 0 else 0.0,
            })
        
        return {
            "total_decisions": total_decisions,
            "average_confidence": avg_confidence,
            "agent_performance": agent_stats,
            "recent_accuracy_trend": recent_accuracy,
        }


def get_required_capabilities_for_task(task_type: str) -> List[str]:
    """
    Get all capabilities required for a specific task type.
    """
    cypher = """
    MATCH (tt:TaskType {name: $taskType})-[:REQUIRES_CAPABILITY]->(cap:Capability)
    RETURN cap.name AS capability
    ORDER BY cap.name
    """
    with _session() as session:
        result = session.run(cypher, taskType=task_type)
        return [record["capability"] for record in result]


def get_agent_capabilities(agent_name: str) -> List[str]:
    """
    Get all capabilities that an agent has.
    """
    cypher = """
    MATCH (agent:Agent {name: $name})-[:HAS_CAPABILITY]->(cap:Capability)
    RETURN cap.name AS capability
    ORDER BY cap.name
    """
    with _session() as session:
        result = session.run(cypher, name=agent_name)
        return [record["capability"] for record in result]


def get_complementary_agents(agent_name: str, task_type: str | None = None, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get agents that complement the given agent based on missing capabilities for the task.
    Finds agents that have capabilities required by the task but not satisfied by the primary agent.
    
    Args:
        agent_name: Name of the primary agent
        task_type: Optional task type to determine required capabilities
        limit: Maximum number of complementary agents to return
    
    Returns:
        List of complementary agents with their details and missing capabilities they provide
    """
    if not task_type:
        # If no task type, return empty list (can't determine missing capabilities)
        return []
    
    cypher = """
    // Get required capabilities for the task
    MATCH (tt:TaskType {name: $taskType})-[:REQUIRES_CAPABILITY]->(reqCap:Capability)
    WITH collect(DISTINCT reqCap.name) AS requiredCapabilities
    
    // Get capabilities that the primary agent has
    MATCH (primary:Agent {name: $name})-[:HAS_CAPABILITY]->(primaryCap:Capability)
    WITH requiredCapabilities, collect(DISTINCT primaryCap.name) AS primaryCapabilities
    
    // Find missing capabilities (required but not in primary agent's capabilities)
    WITH requiredCapabilities, primaryCapabilities,
         [cap IN requiredCapabilities WHERE NOT cap IN primaryCapabilities] AS missingCapabilities
    
    // Find agents that have at least one missing capability
    MATCH (complement:Agent)-[:HAS_CAPABILITY]->(compCap:Capability)
    WHERE compCap.name IN missingCapabilities AND complement.name <> $name
    
    // Collect all capabilities for each complementary agent
    WITH complement, missingCapabilities,
         collect(DISTINCT compCap.name) AS allCapabilities,
         [cap IN collect(DISTINCT compCap.name) WHERE cap IN missingCapabilities] AS matchingMissingCapabilities
    
    // Only return agents that have at least one missing capability
    WHERE size(matchingMissingCapabilities) > 0
    
    RETURN complement.name AS name,
           complement.description AS description,
           complement.capabilityLevel AS capabilityLevel,
           complement.domainExpertise AS domainExpertise,
           complement.historicalAccuracy AS historicalAccuracy,
           allCapabilities AS capabilities,
           matchingMissingCapabilities AS missingCapabilitiesProvided,
           size(matchingMissingCapabilities) AS missingCapabilityCount
    
    ORDER BY missingCapabilityCount DESC, capabilityLevel DESC, historicalAccuracy DESC
    LIMIT $limit
    """
    with _session() as session:
        result = session.run(cypher, name=agent_name, taskType=task_type, limit=limit)
        complementary = []
        for record in result:
            complementary.append({
                "name": record["name"],
                "description": record.get("description", ""),
                "capability_level": record.get("capabilityLevel", 0.5),
                "domain_expertise": record.get("domainExpertise", "general"),
                "historical_accuracy": record.get("historicalAccuracy", 0.5),
                "capabilities": [c for c in record["capabilities"] if c],
                "missing_capabilities": [c for c in record["missingCapabilitiesProvided"] if c],
            })
        return complementary

