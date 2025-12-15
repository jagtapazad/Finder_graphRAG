import React, { useEffect, useState } from "react";
import { RoutingMetrics } from "../types";

export const MetricsDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<RoutingMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await fetch("/metrics/");
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Metrics fetch error:", response.status, errorText);
        throw new Error(`Failed to fetch metrics: ${response.status} ${errorText.substring(0, 100)}`);
      }
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const text = await response.text();
        throw new Error(`Expected JSON but got: ${contentType}. Response: ${text.substring(0, 200)}`);
      }
      const data = await response.json();
      setMetrics(data);
    } catch (err) {
      console.error("Metrics fetch error:", err);
      setError(err instanceof Error ? err.message : "Failed to load metrics");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="metrics-dashboard">
        <h3>Routing Metrics</h3>
        <p className="muted">Loading metrics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="metrics-dashboard">
        <h3>Routing Metrics</h3>
        <div className="error-banner">{error}</div>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="metrics-dashboard">
        <h3>Routing Metrics</h3>
        <p className="muted">No metrics available</p>
      </div>
    );
  }

  return (
    <div className="metrics-dashboard">
      <h3>Routing Metrics Dashboard</h3>

      <div className="metrics-summary">
        <div className="metric-card">
          <h4>Total Decisions</h4>
          <p className="metric-value">{metrics.total_decisions}</p>
        </div>
        <div className="metric-card">
          <h4>Average Confidence</h4>
          <p className="metric-value">
            {(metrics.average_confidence * 100).toFixed(1)}%
          </p>
        </div>
      </div>

      <div className="agent-performance-section">
        <h4>Agent Performance</h4>
        {metrics.agent_performance.length === 0 ? (
          <p className="muted">No performance data available yet</p>
        ) : (
          <div className="performance-table-wrapper">
            <table className="performance-table">
              <thead>
                <tr>
                  <th>Agent</th>
                  <th>Total</th>
                  <th>Successes</th>
                  <th>Failures</th>
                  <th>Success Rate</th>
                </tr>
              </thead>
              <tbody>
                {metrics.agent_performance.map((agent) => (
                  <tr key={agent.agent_name}>
                    <td>{agent.agent_name}</td>
                    <td>{agent.total}</td>
                    <td className="success">{agent.successes}</td>
                    <td className="failure">{agent.failures}</td>
                    <td>
                      <strong>{(agent.success_rate * 100).toFixed(1)}%</strong>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="accuracy-trend-section">
        <h4>Recent Accuracy Trend (Last 30 Days)</h4>
        {metrics.recent_accuracy_trend.length === 0 ? (
          <p className="muted">No trend data available yet</p>
        ) : (
          <div className="trend-chart">
            {metrics.recent_accuracy_trend.map((day) => (
              <div key={day.day} className="trend-bar-container">
                <div className="trend-bar-label">{day.day}</div>
                <div className="trend-bar">
                  <div
                    className="trend-bar-fill"
                    style={{
                      width: `${day.accuracy * 100}%`,
                      backgroundColor: day.accuracy > 0.8 ? "#4CAF50" : day.accuracy > 0.6 ? "#FFC107" : "#F44336",
                    }}
                  >
                    <span className="trend-bar-text">
                      {(day.accuracy * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                <div className="trend-bar-count">
                  {day.successes}/{day.total}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

