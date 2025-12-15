from fastapi import APIRouter, HTTPException

from ...kg.queries import (
    get_agents_by_task_type,
    get_required_capabilities_for_task,
    get_agent_capabilities,
    get_complementary_agents,
    _session,
)

router = APIRouter()


@router.get("/")
def list_agents(task_type: str | None = None) -> list[dict]:
    """
    List all agents or filter by task type.
    Returns agents with all their properties including descriptions.
    """
    try:
        if task_type:
            agents = get_agents_by_task_type(task_type)
            return [a.__dict__ for a in agents]
        
        # Return all agents if no task_type specified
        cypher = """
        MATCH (agent:Agent)
        OPTIONAL MATCH (agent)-[:HAS_CAPABILITY]->(cap:Capability)
        WITH agent, collect(DISTINCT cap.name) AS capabilities
        RETURN agent, capabilities
        ORDER BY agent.name
        """
        with _session() as session:
            result = session.run(cypher)
            agents = []
            for record in result:
                node = record["agent"]
                capabilities = [c for c in record["capabilities"] if c]  # Filter out None values
                
                # Parse tags by category
                tags = node.get("tags", [])
                tag_categories = {
                    "industry": [],
                    "domain": [],
                    "capability": [],
                    "purpose": []
                }
                
                for tag in tags:
                    if isinstance(tag, str) and ":" in tag:
                        category, value = tag.split(":", 1)
                        if category in tag_categories:
                            tag_categories[category].append(value)
                
                # Get all properties from the node, including enhanced query matching properties
                agent_dict = {
                    "name": node.get("name", "Unknown"),
                    "capability_level": node.get("capabilityLevel", 0.5),
                    "domain_expertise": node.get("domainExpertise", "general"),
                    "input_format": node.get("inputFormat", "text"),
                    "output_format": node.get("outputFormat", "text"),
                    "historical_accuracy": node.get("historicalAccuracy", 0.5),
                    "response_time": node.get("responseTime", 1.0),
                    "cost_efficiency": node.get("costEfficiency", 0.5),
                    "reliability": node.get("reliability", 0.5),
                    "specialization_score": node.get("specializationScore", 0.5),
                    "description": node.get("description", ""),
                    "success_count": node.get("successCount", 0),
                    "failure_count": node.get("failureCount", 0),
                    "capabilities": capabilities,
                    "tags": tags,
                    "tag_categories": tag_categories,
                }
                # Add enhanced query matching properties if they exist
                if "keywords" in node:
                    agent_dict["keywords"] = node["keywords"]
                if "queryPatterns" in node:
                    agent_dict["query_patterns"] = node["queryPatterns"]
                if "useCases" in node:
                    agent_dict["use_cases"] = node["useCases"]
                agents.append(agent_dict)
            return agents
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching agents: {str(e)}"
        )


@router.get("/{agent_name}")
def get_agent_details(agent_name: str) -> dict:
    """
    Get detailed information about a specific agent including capabilities and tags.
    """
    try:
        cypher = """
        MATCH (agent:Agent {name: $name})
        OPTIONAL MATCH (agent)-[:HAS_CAPABILITY]->(cap:Capability)
        RETURN agent, collect(DISTINCT cap.name) AS capabilities
        """
        with _session() as session:
            result = session.run(cypher, name=agent_name)
            record = result.single()
            if not record:
                raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
            
            node = record["agent"]
            capabilities = [c for c in record["capabilities"] if c]  # Filter out None values
            
            # Parse tags by category
            tags = node.get("tags", [])
            tag_categories = {
                "industry": [],
                "domain": [],
                "capability": [],
                "purpose": []
            }
            
            for tag in tags:
                if isinstance(tag, str) and ":" in tag:
                    category, value = tag.split(":", 1)
                    if category in tag_categories:
                        tag_categories[category].append(value)
            
            return {
                "name": node["name"],
                "capability_level": node.get("capabilityLevel", 0.5),
                "domain_expertise": node.get("domainExpertise", "general"),
                "input_format": node.get("inputFormat", "text"),
                "output_format": node.get("outputFormat", "text"),
                "historical_accuracy": node.get("historicalAccuracy", 0.5),
                "response_time": node.get("responseTime", 1.0),
                "cost_efficiency": node.get("costEfficiency", 0.5),
                "reliability": node.get("reliability", 0.5),
                "specialization_score": node.get("specializationScore", 0.5),
                "description": node.get("description", ""),
                "success_count": node.get("successCount", 0),
                "failure_count": node.get("failureCount", 0),
                "capabilities": capabilities,
                "tags": tags,
                "tag_categories": tag_categories,
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching agent details: {str(e)}"
        )


@router.get("/{agent_name}/capabilities")
def get_agent_capabilities_endpoint(agent_name: str) -> dict:
    """
    Get all capabilities for a specific agent.
    """
    try:
        capabilities = get_agent_capabilities(agent_name)
        return {
            "agent_name": agent_name,
            "capabilities": capabilities,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching agent capabilities: {str(e)}"
        )


@router.get("/{agent_name}/complementary")
def get_complementary_agents_endpoint(agent_name: str, task_type: str | None = None, limit: int = 5) -> dict:
    """
    Get agents that complement the given agent based on missing capabilities for the task.
    """
    try:
        complementary = get_complementary_agents(agent_name, task_type=task_type, limit=limit)
        return {
            "primary_agent": agent_name,
            "task_type": task_type,
            "complementary_agents": complementary,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching complementary agents: {str(e)}"
        )


@router.get("/task-types/{task_type}/required-capabilities")
def get_required_capabilities_endpoint(task_type: str) -> dict:
    """
    Get all capabilities required for a specific task type.
    """
    try:
        capabilities = get_required_capabilities_for_task(task_type)
        return {
            "task_type": task_type,
            "required_capabilities": capabilities,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching required capabilities: {str(e)}"
        )


