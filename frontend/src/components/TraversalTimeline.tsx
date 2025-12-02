import React from "react";
import { RoutingResult } from "../types";

type Props = {
  result: RoutingResult;
  hasCandidates: boolean;
};

export const TraversalTimeline: React.FC<Props> = ({
  result,
  hasCandidates,
}) => {
  const { chosen_agent, confidence, rationale } = result;
  const { analyzed_query, top_candidates } = rationale;

  const steps = [
    {
      title: "1. User query received",
      description: "The raw text you entered is captured as a Query node.",
      details: analyzed_query.raw_text,
    },
    {
      title: "2. QueryAnalyzer extracts task metadata",
      description:
        "An LLM-based extractor identifies task type, complexity, domain, and output preferences.",
      details: `TaskType: ${analyzed_query.task_type}, Complexity: ${analyzed_query.complexity.toFixed(
        2
      )}, Domain: ${analyzed_query.domain}`,
    },
    {
      title: "3. Knowledge graph traversal",
      description:
        "The router walks the graph from TaskType → required Capabilities → Agents that have those capabilities.",
      details: hasCandidates
        ? `Found ${top_candidates.length} candidate agents connected to the required capabilities for ${analyzed_query.task_type}.`
        : "No agents matched the required capabilities for this task type.",
    },
    {
      title: "4. Scoring & ranking",
      description:
        "Each candidate agent is scored using capability level, historical accuracy, and domain fit.",
      details: hasCandidates
        ? top_candidates
            .map(
              (c, idx) =>
                `${idx + 1}. ${c.name} (score: ${c.score.toFixed(3)})`
            )
            .join("  ·  ")
        : "No candidates to score – a fallback strategy is applied.",
    },
    {
      title: "5. Fallback & final selection",
      description:
        "If the best score is below the confidence threshold, the router follows FALLBACK_AGENT links to choose a safer agent.",
      details: `Chosen agent: ${chosen_agent}  ·  Confidence: ${(confidence * 100).toFixed(
        1
      )}%.`,
    },
  ];

  return (
    <div className="timeline-section">
      <h3>Graph traversal & routing reasoning</h3>
      <ol className="timeline">
        {steps.map((step, idx) => (
          <li key={idx} className="timeline-step">
            <div className="timeline-badge">{idx + 1}</div>
            <div className="timeline-content">
              <h4>{step.title}</h4>
              <p className="muted">{step.description}</p>
              <p className="timeline-details">{step.details}</p>
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
};


