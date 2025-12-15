"""
Key Cypher Queries for Smart Agentic Router

This module documents the 5 core Cypher queries that drive the routing system.
These queries demonstrate SPARQL-driven design thinking adapted for Neo4j/Cypher.

Query 1: Find agents by task type with capability threshold
Query 2: Find similar agents for fallback scenarios
Query 3: Retrieve historical routing decisions for learning
Query 4: Find agents by domain expertise
Query 5: Get routing path explanation (for explainability)
"""

# Query 1: Find best agents for a task type with minimum capability threshold
# Purpose: Core routing query - finds agents that have required capabilities
# Returns: Agents sorted by capability level
QUERY_1_FIND_AGENTS_BY_TASK = """
MATCH (tt:TaskType {name: $taskType})-[:REQUIRES_CAPABILITY]->(cap:Capability),
      (agent:Agent)-[:HAS_CAPABILITY]->(cap)
WITH DISTINCT agent, agent.capabilityLevel AS capLevel
WHERE capLevel >= $minThreshold
RETURN agent, capLevel, agent.historicalAccuracy AS histAcc, agent.domainExpertise AS domain
ORDER BY capLevel DESC, histAcc DESC
"""

# Query 2: Find similar agents for fallback scenarios
# Purpose: When primary agent fails, find agents with overlapping capabilities
# Returns: Agents sorted by shared capability count
QUERY_2_FIND_SIMILAR_AGENTS = """
MATCH (a1:Agent {name: $agentName})-[:HAS_CAPABILITY]->(cap:Capability)<-[:HAS_CAPABILITY]-(a2:Agent)
WHERE a1 <> a2
WITH a2, count(DISTINCT cap) AS sharedCaps, a2.capabilityLevel AS capLevel, a2.historicalAccuracy AS histAcc
ORDER BY sharedCaps DESC, capLevel DESC, histAcc DESC
RETURN a2, sharedCaps
LIMIT 3
"""

# Query 3: Retrieve historical routing decisions for learning
# Purpose: Analyze past routing decisions to improve future routing
# Returns: Historical decisions with outcomes for performance analysis
QUERY_3_HISTORICAL_DECISIONS = """
MATCH (rd:RoutingDecision)-[:ROUTED_TO]->(agent:Agent {name: $agentName})
OPTIONAL MATCH (rd)-[:SOURCE_QUERY]->(q:Query)
WHERE rd.outcome IS NOT NULL AND rd.outcome <> 'PENDING'
RETURN rd.id AS decisionId, rd.confidence AS confidence, rd.outcome AS outcome, rd.timestamp AS timestamp, q AS query
ORDER BY rd.timestamp DESC
LIMIT 50
"""

# Query 4: Find agents by domain expertise
# Purpose: Route queries to domain-specialized agents or general agents
# Returns: Agents matching domain, sorted by historical accuracy
QUERY_4_AGENTS_BY_DOMAIN = """
MATCH (agent:Agent)
WHERE agent.domainExpertise = $domain OR agent.domainExpertise = 'general'
RETURN agent, agent.capabilityLevel AS capLevel, agent.historicalAccuracy AS histAcc
ORDER BY 
  CASE WHEN agent.domainExpertise = $domain THEN 1 ELSE 2 END,
  histAcc DESC,
  capLevel DESC
"""

# Query 5: Get routing path explanation (for explainability)
# Purpose: Show the complete graph traversal explaining why an agent was chosen
# Returns: Agent details with matching capabilities and reasoning path
QUERY_5_ROUTING_EXPLANATION = """
MATCH (rd:RoutingDecision {id: $rdId})-[:ROUTED_TO]->(agent:Agent)
OPTIONAL MATCH (rd)-[:SOURCE_QUERY]->(q:Query)
OPTIONAL MATCH (agent)-[:HAS_CAPABILITY]->(cap:Capability)
OPTIONAL MATCH (tt:TaskType {name: $taskType})-[:REQUIRES_CAPABILITY]->(reqCap:Capability)
WITH agent, q, rd, 
     collect(DISTINCT cap.name) AS allCapabilities,
     collect(DISTINCT reqCap.name) AS requiredCapabilities
WITH agent, q, rd, allCapabilities, requiredCapabilities,
     [cap IN allCapabilities WHERE cap IN requiredCapabilities] AS matchingCapabilities
RETURN agent.name AS agentName,
       coalesce(agent.capabilityLevel, 0.5) AS capabilityLevel,
       coalesce(agent.historicalAccuracy, 0.5) AS historicalAccuracy,
       coalesce(agent.domainExpertise, 'general') AS domainExpertise,
       coalesce(q.text, '') AS queryText,
       coalesce(rd.confidence, 0.5) AS confidence,
       coalesce(allCapabilities, []) AS allCapabilities,
       coalesce(matchingCapabilities, []) AS matchingCapabilities,
       size(coalesce(matchingCapabilities, [])) AS matchingCapabilityCount
"""

# Query 6: Get full graph traversal path for visualization
# Purpose: Show the complete path from Query -> TaskType -> Capabilities -> Agent
QUERY_6_ROUTING_PATH = """
MATCH (rd:RoutingDecision {id: $rdId})-[:SOURCE_QUERY]->(q:Query)
MATCH (rd)-[:ROUTED_TO]->(agent:Agent)
OPTIONAL MATCH (tt:TaskType {name: $taskType})-[:REQUIRES_CAPABILITY]->(reqCap:Capability)
OPTIONAL MATCH (agent)-[:HAS_CAPABILITY]->(agentCap:Capability)
RETURN q.text AS queryText,
       $taskType AS taskType,
       collect(DISTINCT reqCap.name) AS requiredCapabilities,
       agent.name AS selectedAgent,
       collect(DISTINCT agentCap.name) AS agentCapabilities,
       [cap IN collect(DISTINCT agentCap) WHERE cap IN collect(DISTINCT reqCap) | cap.name] AS matchingCapabilities
"""

