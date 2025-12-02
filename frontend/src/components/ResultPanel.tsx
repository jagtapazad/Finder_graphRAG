import React from "react";
import { RoutingResult } from "../types";
import { TraversalTimeline } from "./TraversalTimeline";

type Props = {
  result: RoutingResult;
};

export const ResultPanel: React.FC<Props> = ({ result }) => {
  const { chosen_agent, confidence, rationale } = result;
  const { analyzed_query, top_candidates } = rationale;

  const confidencePct = Math.round(confidence * 100);

  return (
    <div className="result-root">
      <div className="result-summary">
        <div>
          <h2>Selected Agent</h2>
          <p className="agent-name">{chosen_agent}</p>
          <p className="confidence">
            Confidence: <strong>{confidencePct}%</strong>
          </p>
        </div>
        <div className="analyzed-card">
          <h3>Query understanding</h3>
          <dl>
            <div>
              <dt>Detected task type</dt>
              <dd>{analyzed_query.task_type}</dd>
            </div>
            <div>
              <dt>Complexity</dt>
              <dd>{analyzed_query.complexity.toFixed(2)}</dd>
            </div>
            <div>
              <dt>Domain</dt>
              <dd>{analyzed_query.domain}</dd>
            </div>
            {analyzed_query.output_format && (
              <div>
                <dt>Preferred output</dt>
                <dd>{analyzed_query.output_format}</dd>
              </div>
            )}
          </dl>
        </div>
      </div>

      <div className="candidates-section">
        <h3>Top candidate agents</h3>
        {top_candidates.length === 0 ? (
          <p className="muted">
            No candidates were returned by the knowledge graph. A fallback
            strategy was likely used.
          </p>
        ) : (
          <div className="candidate-grid">
            {top_candidates.map((c) => (
              <div
                key={c.name}
                className={
                  c.name === chosen_agent
                    ? "candidate-card candidate-card--chosen"
                    : "candidate-card"
                }
              >
                <div className="candidate-name-row">
                  <span className="candidate-name">{c.name}</span>
                  {c.name === chosen_agent && (
                    <span className="pill pill-primary">Selected</span>
                  )}
                </div>
                <p className="candidate-score">
                  Overall score: <strong>{c.score.toFixed(3)}</strong>
                </p>
                <p className="muted small">
                  Combines capability level, historical accuracy, and domain
                  match.
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      <TraversalTimeline
        result={result}
        hasCandidates={top_candidates.length > 0}
      />
    </div>
  );
};


