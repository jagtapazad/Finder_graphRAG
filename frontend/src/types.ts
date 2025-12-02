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
};

export type RoutingResult = {
  routing_decision_id: string;
  chosen_agent: string;
  confidence: number;
  rationale: {
    analyzed_query: AnalyzedQuery;
    top_candidates: TopCandidate[];
  };
};


