import React, { useState, useEffect } from "react";
import { RoutingResult } from "../types";
import { WorkflowTile } from "./WorkflowTile";

type Props = {
  result: RoutingResult;
};

type ComplementaryAgent = {
  name: string;
  description: string;
  capability_level: number;
  domain_expertise: string;
  historical_accuracy: number;
  capabilities: string[];
  missing_capabilities?: string[];
};

export const ResultPanel: React.FC<Props> = ({ result }) => {
  const { chosen_agent, confidence, rationale } = result;
  const { analyzed_query, top_candidates, task_type } = rationale;

  // New state for capabilities and complementary agents
  const [requiredCapabilities, setRequiredCapabilities] = useState<string[]>([]);
  const [agentCapabilities, setAgentCapabilities] = useState<string[]>([]);
  const [complementaryAgents, setComplementaryAgents] = useState<ComplementaryAgent[]>([]);
  const [loadingCapabilities, setLoadingCapabilities] = useState(false);

  // Fetch capabilities and complementary agents when component mounts or agent changes
  useEffect(() => {
    const fetchCapabilities = async () => {
      setLoadingCapabilities(true);
      try {
        const taskTypeToUse = task_type || analyzed_query.task_type;
        
        // Fetch required capabilities for task type
        const reqCapsResponse = await fetch(
          `/agents/task-types/${encodeURIComponent(taskTypeToUse)}/required-capabilities`
        );
        if (reqCapsResponse.ok) {
          const reqCapsData = await reqCapsResponse.json();
          setRequiredCapabilities(reqCapsData.required_capabilities || []);
        }

        // Fetch agent capabilities
        const agentCapsResponse = await fetch(
          `/agents/${encodeURIComponent(chosen_agent)}/capabilities`
        );
        if (agentCapsResponse.ok) {
          const agentCapsData = await agentCapsResponse.json();
          setAgentCapabilities(agentCapsData.capabilities || []);
        }

        // Fetch complementary agents (based on missing capabilities for the task)
        const compAgentsResponse = await fetch(
          `/agents/${encodeURIComponent(chosen_agent)}/complementary?task_type=${encodeURIComponent(taskTypeToUse)}&limit=5`
        );
        if (compAgentsResponse.ok) {
          const compAgentsData = await compAgentsResponse.json();
          setComplementaryAgents(compAgentsData.complementary_agents || []);
        }
      } catch (err) {
        console.error("Failed to fetch capabilities:", err);
      } finally {
        setLoadingCapabilities(false);
      }
    };

    fetchCapabilities();
  }, [chosen_agent, task_type, analyzed_query.task_type]);

  const confidencePct = Math.round(confidence * 100);

  return (
    <div className="result-root">
      {/* Individual Tiles */}
      <div className="result-tiles-grid">
        {/* Selected Agent Tile */}
        <div className="result-tile result-tile--agent">
          <h3 className="result-tile-title">Selected Agent</h3>
          <p className="agent-name">{chosen_agent}</p>
          <p className="confidence">
            Confidence: <strong>{confidencePct}%</strong>
          </p>
        </div>

        {/* Query Understanding Tile */}
        <div className="result-tile result-tile--query">
          <h3 className="result-tile-title">Query Understanding</h3>
          <dl className="query-details">
            <div>
              <dt>Task Type</dt>
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
                <dt>Output Format</dt>
                <dd>{analyzed_query.output_format}</dd>
              </div>
            )}
          </dl>
        </div>

        {/* Workflow Tile */}
        <WorkflowTile />
      </div>

      {/* Capabilities Section */}
      <div className="capabilities-section">
        <h3>Capabilities Analysis</h3>
        <div className="capabilities-grid">
          {/* Required Capabilities for Task */}
          <div className="capability-card">
            <h4 className="capability-card-title">
              Required for {task_type || analyzed_query.task_type}
            </h4>
            {loadingCapabilities ? (
              <p className="muted">Loading...</p>
            ) : requiredCapabilities.length > 0 ? (
              <div className="capability-tags">
                {requiredCapabilities.map((cap, idx) => (
                  <span key={idx} className="capability-tag capability-tag--required">
                    {cap}
                  </span>
                ))}
              </div>
            ) : (
              <p className="muted">No required capabilities found</p>
            )}
          </div>

          {/* Agent Capabilities */}
          <div className="capability-card">
            <h4 className="capability-card-title">
              {chosen_agent} Capabilities
            </h4>
            {loadingCapabilities ? (
              <p className="muted">Loading...</p>
            ) : agentCapabilities.length > 0 ? (
              <div className="capability-tags">
                {agentCapabilities.map((cap, idx) => {
                  const isMatching = requiredCapabilities.includes(cap);
                  return (
                    <span
                      key={idx}
                      className={`capability-tag ${
                        isMatching
                          ? "capability-tag--matching"
                          : "capability-tag--agent"
                      }`}
                      title={isMatching ? "Matches required capability" : ""}
                    >
                      {cap}
                      {isMatching && " ✓"}
                    </span>
                  );
                })}
              </div>
            ) : (
              <p className="muted">No capabilities found</p>
            )}
          </div>
        </div>
      </div>

      {/* Top Candidates Section */}
      <div className="candidates-section">
        <h3>Top Candidate Agents</h3>
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
                {c.tie_breaking && (
                  <div className="candidate-details">
                    <div className="candidate-metric">
                      <span className="metric-label">Capability:</span>
                      <span className="metric-value">
                        {(c.tie_breaking.capability_level * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="candidate-metric">
                      <span className="metric-label">Accuracy:</span>
                      <span className="metric-value">
                        {(c.tie_breaking.historical_accuracy * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="candidate-metric">
                      <span className="metric-label">Reliability:</span>
                      <span className="metric-value">
                        {(c.tie_breaking.reliability * 100).toFixed(0)}%
                      </span>
                    </div>
                    {c.tie_breaking.domain_exact_match > 0 && (
                      <div className="candidate-metric">
                        <span className="metric-label">Domain:</span>
                        <span className="metric-value">Exact match</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Complementary Agents Section */}
      {complementaryAgents.length > 0 && (
        <div className="complementary-section">
          <h3>Complementary Agents</h3>
          <p className="section-description">
            These agents provide capabilities that <strong>{chosen_agent}</strong>{" "}
            lacks for this task, helping to complete the required capabilities.
          </p>
          <div className="complementary-grid">
            {complementaryAgents.map((agent) => (
              <div key={agent.name} className="complementary-card">
                <div className="complementary-header">
                  <h4 className="complementary-name">{agent.name}</h4>
                  <span
                    className={`agent-badge agent-badge--${agent.domain_expertise}`}
                  >
                    {agent.domain_expertise}
                  </span>
                </div>
                {agent.description && (
                  <p className="complementary-description">
                    {agent.description}
                  </p>
                )}
                {agent.missing_capabilities && agent.missing_capabilities.length > 0 && (
                  <div className="complementary-missing-caps">
                    <strong>Provides Missing Capabilities:</strong>
                    <div className="capability-tags">
                      {agent.missing_capabilities.map((cap, idx) => (
                        <span
                          key={idx}
                          className="capability-tag capability-tag--matching capability-tag--small"
                        >
                          {cap}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                <div className="complementary-metrics">
                  <div className="complementary-metric">
                    <span className="metric-label">Capability:</span>
                    <span className="metric-value">
                      {(agent.capability_level * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="complementary-metric">
                    <span className="metric-label">Accuracy:</span>
                    <span className="metric-value">
                      {(agent.historical_accuracy * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                {agent.capabilities.length > 0 && (
                  <div className="complementary-capabilities">
                    <strong>All Capabilities:</strong>
                    <div className="capability-tags">
                      {agent.capabilities.slice(0, 3).map((cap, idx) => (
                        <span
                          key={idx}
                          className="capability-tag capability-tag--small"
                        >
                          {cap}
                        </span>
                      ))}
                      {agent.capabilities.length > 3 && (
                        <span className="capability-tag capability-tag--small">
                          +{agent.capabilities.length - 3} more
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};


