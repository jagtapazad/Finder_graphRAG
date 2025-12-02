// 1. Clean DB
MATCH (n) DETACH DELETE n;

// 2. Capabilities
CREATE (webCap:Capability {name: 'WebSearching'});
CREATE (factCap:Capability {name: 'FactRetrieval'});
CREATE (codeCap:Capability {name: 'CodeUnderstanding'});
CREATE (debugCap:Capability {name: 'DebuggingAssistance'});
CREATE (sumCap:Capability {name: 'DocumentSummarization'});
CREATE (vizCap:Capability {name: 'DataVisualization'});
CREATE (genCap:Capability {name: 'GeneralKnowledge'});

// 3. Agents (subset; extend as needed)
CREATE (web:SpecializedAgent:Agent {
  name: 'WebSearchAgent',
  capabilityLevel: 0.9,
  inputFormat: 'text',
  outputFormat: 'structured_results',
  domainExpertise: 'general',
  successCount: 0,
  failureCount: 0,
  historicalAccuracy: 0.5
});

CREATE (code:SpecializedAgent:Agent {
  name: 'CodeAnalysisAgent',
  capabilityLevel: 0.85,
  inputFormat: 'code',
  outputFormat: 'analysis',
  domainExpertise: 'technical',
  successCount: 0,
  failureCount: 0,
  historicalAccuracy: 0.5
});

CREATE (sum:SpecializedAgent:Agent {
  name: 'SummarizationAgent',
  capabilityLevel: 0.83,
  inputFormat: 'text',
  outputFormat: 'summary',
  domainExpertise: 'general',
  successCount: 0,
  failureCount: 0,
  historicalAccuracy: 0.5
});

CREATE (viz:SpecializedAgent:Agent {
  name: 'DataVisualizationAgent',
  capabilityLevel: 0.8,
  inputFormat: 'data',
  outputFormat: 'visualization',
  domainExpertise: 'technical',
  successCount: 0,
  failureCount: 0,
  historicalAccuracy: 0.5
});

CREATE (perp:SpecializedAgent:Agent {
  name: 'PerplexityFallbackAgent',
  capabilityLevel: 0.8,
  inputFormat: 'text',
  outputFormat: 'answer',
  domainExpertise: 'general',
  successCount: 0,
  failureCount: 0,
  historicalAccuracy: 0.5
});

// 4. HAS_CAPABILITY relationships
MATCH (web:Agent {name: 'WebSearchAgent'}), (webCap:Capability {name: 'WebSearching'})
CREATE (web)-[:HAS_CAPABILITY]->(webCap);

MATCH (web:Agent {name: 'WebSearchAgent'}), (factCap:Capability {name: 'FactRetrieval'})
CREATE (web)-[:HAS_CAPABILITY]->(factCap);

MATCH (code:Agent {name: 'CodeAnalysisAgent'}), (codeCap:Capability {name: 'CodeUnderstanding'})
CREATE (code)-[:HAS_CAPABILITY]->(codeCap);

MATCH (code:Agent {name: 'CodeAnalysisAgent'}), (debugCap:Capability {name: 'DebuggingAssistance'})
CREATE (code)-[:HAS_CAPABILITY]->(debugCap);

MATCH (sum:Agent {name: 'SummarizationAgent'}), (sumCap:Capability {name: 'DocumentSummarization'})
CREATE (sum)-[:HAS_CAPABILITY]->(sumCap);

MATCH (viz:Agent {name: 'DataVisualizationAgent'}), (vizCap:Capability {name: 'DataVisualization'})
CREATE (viz)-[:HAS_CAPABILITY]->(vizCap);

MATCH (perp:Agent {name: 'PerplexityFallbackAgent'}), (genCap:Capability {name: 'GeneralKnowledge'})
CREATE (perp)-[:HAS_CAPABILITY]->(genCap);

// 5. TaskTypes
CREATE (webTask:TaskType {name: 'WebSearchTask', complexityLevel: 0.3});
CREATE (codeDebugTask:TaskType {name: 'CodeDebuggingTask', complexityLevel: 0.8});
CREATE (sumTask:TaskType {name: 'SummarizationTask', complexityLevel: 0.5});
CREATE (vizTask:TaskType {name: 'VisualizationTask', complexityLevel: 0.7});

MATCH (webTask),(webCap) CREATE (webTask)-[:REQUIRES_CAPABILITY]->(webCap);
MATCH (codeDebugTask),(codeCap) CREATE (codeDebugTask)-[:REQUIRES_CAPABILITY]->(codeCap);
MATCH (codeDebugTask),(debugCap) CREATE (codeDebugTask)-[:REQUIRES_CAPABILITY]->(debugCap);
MATCH (sumTask),(sumCap) CREATE (sumTask)-[:REQUIRES_CAPABILITY]->(sumCap);
MATCH (vizTask),(vizCap) CREATE (vizTask)-[:REQUIRES_CAPABILITY]->(vizCap);

// 6. Fallbacks
MATCH (web:Agent {name:'WebSearchAgent'}),
      (perp:Agent {name:'PerplexityFallbackAgent'})
CREATE (web)-[:FALLBACK_AGENT]->(perp);

MATCH (code:Agent {name:'CodeAnalysisAgent'}),
      (perp:Agent {name:'PerplexityFallbackAgent'})
CREATE (code)-[:FALLBACK_AGENT]->(perp);

MATCH (sum:Agent {name:'SummarizationAgent'}),
      (web:Agent {name:'WebSearchAgent'})
CREATE (sum)-[:FALLBACK_AGENT]->(web);

MATCH (viz:Agent {name:'DataVisualizationAgent'}),
      (sum:Agent {name:'SummarizationAgent'})
CREATE (viz)-[:FALLBACK_AGENT]->(sum);

// 7. Sample RoutingDecision
CREATE (q1:Query {text: 'Find latest LLM pruning research'});
CREATE (rd1:RoutingDecision {timestamp: datetime(), confidence: 0.82, outcome: 'SUCCESS'});

MATCH (web),(q1)
CREATE (rd1)-[:SOURCE_QUERY]->(q1);
CREATE (rd1)-[:ROUTED_TO]->(web);


