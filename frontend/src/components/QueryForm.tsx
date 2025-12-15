import React, { useState, useEffect } from "react";
import { RoutingResult, RoutingExplanation } from "../types";
import { TraversalTimeline } from "./TraversalTimeline";

type Props = {
  onSubmit: (query: string) => void | Promise<void>;
  loading: boolean;
  result: RoutingResult | null;
};

export const QueryForm: React.FC<Props> = ({ onSubmit, loading, result }) => {
  const [query, setQuery] = useState("");
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  const [feedbackError, setFeedbackError] = useState<string | null>(null);

  // Routing explanation & traversal state (for buttons below feedback)
  const [explanation, setExplanation] = useState<RoutingExplanation | null>(
    null
  );
  const [loadingExplanation, setLoadingExplanation] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [showTraversal, setShowTraversal] = useState(false);
  const [explanationError, setExplanationError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    
    // Reset feedback and explanation when new query is submitted
    setFeedbackSubmitted(false);
    setFeedbackError(null);
    setExplanation(null);
    setShowExplanation(false);
    setShowTraversal(false);
    setExplanationError(null);
    
    // Call onSubmit - this will trigger the API call
    onSubmit(query.trim());
  };

  const handleFeedback = async (success: boolean) => {
    if (!result) return;
    
    setSubmittingFeedback(true);
    setFeedbackError(null);
    
    try {
      const response = await fetch("/feedback/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          routing_decision_id: result.routing_decision_id,
          success: success,
        }),
      });

      if (response.ok) {
        setFeedbackSubmitted(true);
        const data = await response.json();
        console.log("Feedback submitted:", data);
      } else {
        const errorText = await response.text();
        setFeedbackError(`Failed to submit feedback: ${errorText}`);
      }
    } catch (err) {
      console.error("Failed to submit feedback:", err);
      setFeedbackError("Failed to submit feedback. Please try again.");
    } finally {
      setSubmittingFeedback(false);
    }
  };

  const fetchExplanation = async () => {
    if (!result || explanation) return;

    const { routing_decision_id, rationale } = result;
    const { analyzed_query, task_type } = rationale;
    const taskTypeToUse = task_type || analyzed_query.task_type;

    setLoadingExplanation(true);
    setExplanationError(null);
    try {
      const response = await fetch(
        `/explanations/routing/${routing_decision_id}/explanation?task_type=${encodeURIComponent(
          taskTypeToUse
        )}`
      );
      if (response.ok) {
        const data = await response.json();
        setExplanation(data);
        setShowExplanation(true);
      } else {
        const errorText = await response.text();
        console.error(
          "Failed to fetch explanation:",
          response.status,
          errorText
        );
        setExplanationError("Failed to load explanation. Please try again.");
      }
    } catch (err) {
      console.error("Failed to fetch explanation:", err);
      setExplanationError("Failed to load explanation. Please try again.");
    } finally {
      setLoadingExplanation(false);
    }
  };

  const handleShowExplanation = () => {
    if (!result) return;
    if (!showExplanation && !explanation) {
      fetchExplanation();
    } else {
      setShowExplanation(!showExplanation);
    }
    if (!showExplanation) {
      setShowTraversal(false);
    }
  };

  const handleShowTraversal = () => {
    if (!result) return;
    setShowTraversal(!showTraversal);
    if (!showTraversal) {
      setShowExplanation(false);
    }
  };

  // Reset explanation state when result changes (new query submitted)
  useEffect(() => {
    if (result) {
      // Reset explanation-related state when a new result arrives
      setExplanation(null);
      setShowExplanation(false);
      setShowTraversal(false);
      setExplanationError(null);
    }
  }, [result?.routing_decision_id]); // Only reset when routing_decision_id changes

  return (
    <div className="query-form-container">
      <form className="query-form" onSubmit={handleSubmit}>
        <label className="label">
          Enter your task or question
          <textarea
            className="textarea"
            placeholder="e.g., Debug this Python function that keeps timing out..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={4}
            disabled={loading}
          />
        </label>
        <div className="query-form-footer">
          <button className="primary-btn" type="submit" disabled={loading || !query.trim()}>
            {loading ? "Routing..." : "Route to best agent"}
          </button>
          <span className="hint">
            The router will analyze your query, traverse the knowledge graph, and
            explain why it chose a specific agent.
          </span>
        </div>
      </form>

      {/* Feedback Section + routing explanation / traversal */}
      {result && (
        <>
          <div className="feedback-section feedback-section--inline">
            <h4>Provide Feedback</h4>
            {feedbackSubmitted ? (
              <div className="feedback-success">
                <p>
                  ✓ Thank you! Your feedback has been recorded and will improve
                  future routing decisions.
                </p>
              </div>
            ) : (
              <div className="feedback-buttons">
                <button
                  className="feedback-button feedback-button--success"
                  onClick={() => handleFeedback(true)}
                  disabled={submittingFeedback}
                >
                  {submittingFeedback
                    ? "Submitting..."
                    : "✓ Agent worked well"}
                </button>
                <button
                  className="feedback-button feedback-button--failure"
                  onClick={() => handleFeedback(false)}
                  disabled={submittingFeedback}
                >
                  {submittingFeedback
                    ? "Submitting..."
                    : "✗ Agent didn't work well"}
                </button>
              </div>
            )}
            {feedbackError && (
              <div className="error-banner" style={{ marginTop: "0.5rem" }}>
                {feedbackError}
              </div>
            )}
            <p className="muted small" style={{ marginTop: "0.5rem" }}>
              Your feedback helps the system learn and improve routing accuracy
              over time.
            </p>
          </div>

          {/* Buttons & expandable section directly below feedback */}
          <div className="action-buttons-section">
            <div className="action-buttons-group">
              <button
                className={`action-button ${
                  showExplanation ? "action-button--active" : ""
                }`}
                onClick={handleShowExplanation}
                disabled={loadingExplanation}
              >
                {loadingExplanation
                  ? "Loading..."
                  : showExplanation
                  ? "Hide Routing Explanation"
                  : "Show Routing Explanation"}
              </button>
              <button
                className={`action-button ${
                  showTraversal ? "action-button--active" : ""
                }`}
                onClick={handleShowTraversal}
              >
                {showTraversal
                  ? "Hide Graph Traversal"
                  : "Graph Traversal & Routing Reasoning"}
              </button>
            </div>

            <div className="expandable-content">
              {explanationError && (
                <div className="error-banner">{explanationError}</div>
              )}

              {showExplanation && explanation && (
                <div className="explanation-card">
                  <h4>Why {result.chosen_agent} was selected</h4>
                  <dl>
                    <div>
                      <dt>Capability Level</dt>
                      <dd>
                        {(explanation.capability_level * 100).toFixed(1)}%
                      </dd>
                    </div>
                    <div>
                      <dt>Historical Accuracy</dt>
                      <dd>
                        {(explanation.historical_accuracy * 100).toFixed(1)}%
                      </dd>
                    </div>
                    <div>
                      <dt>Domain Expertise</dt>
                      <dd>{explanation.domain_expertise}</dd>
                    </div>
                    <div>
                      <dt>Matching Capabilities</dt>
                      <dd>
                        {explanation.matching_capabilities.length > 0 ? (
                          <ul>
                            {explanation.matching_capabilities.map(
                              (cap, idx) => (
                                <li key={idx}>{cap}</li>
                              )
                            )}
                          </ul>
                        ) : (
                          "None"
                        )}
                      </dd>
                    </div>
                    <div>
                      <dt>All Agent Capabilities</dt>
                      <dd>
                        {explanation.all_capabilities.length > 0 ? (
                          <ul>
                            {explanation.all_capabilities.map((cap, idx) => (
                              <li key={idx}>{cap}</li>
                            ))}
                          </ul>
                        ) : (
                          "None"
                        )}
                      </dd>
                    </div>
                  </dl>
                </div>
              )}

              {showTraversal && (
                <div className="traversal-card">
                  <TraversalTimeline
                    result={result}
                    hasCandidates={
                      result.rationale.top_candidates &&
                      result.rationale.top_candidates.length > 0
                    }
                  />
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};


