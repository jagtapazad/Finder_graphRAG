export type AnalyzedQuery = {
  raw_text: string;
  task_type: string;
  complexity: number;
  domain: string;
  output_format?: string | null;
};

export type TopCandidate = {
  name: string;
  score: number;
  tie_breaking?: Record<string, any>;
};

export type RoutingResult = {
  routing_decision_id: string;
  chosen_agent: string;
  confidence: number;
  rationale: {
    analyzed_query: AnalyzedQuery;
    top_candidates: TopCandidate[];
    task_type?: string;
    tie_breaking_info?: Record<string, any>;
  };
};

export type RoutingExplanation = {
  agent_name: string;
  capability_level: number;
  historical_accuracy: number;
  domain_expertise: string;
  query_text: string;
  confidence: number;
  all_capabilities: string[];
  matching_capabilities: string[];
  matching_capability_count: number;
};

export type RoutingPath = {
  query_text: string;
  task_type: string;
  required_capabilities: string[];
  selected_agent: string;
  agent_capabilities: string[];
  matching_capabilities: string[];
};

export type KGNode = {
  id: string;
  label: string;
  type: string;
  properties: Record<string, any>;
};

export type KGEdge = {
  id: string;
  source: string;
  target: string;
  type: string;
  properties: Record<string, any>;
};

export type KGVisualization = {
  nodes: KGNode[];
  edges: KGEdge[];
};

export type AgentPerformance = {
  agent_name: string;
  total: number;
  successes: number;
  failures: number;
  success_rate: number;
};

export type AccuracyTrend = {
  day: string;
  total: number;
  successes: number;
  accuracy: number;
};

export type RoutingMetrics = {
  total_decisions: number;
  average_confidence: number;
  agent_performance: AgentPerformance[];
  recent_accuracy_trend: AccuracyTrend[];
};


