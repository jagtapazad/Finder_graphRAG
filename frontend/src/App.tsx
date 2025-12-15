import React, { useState } from "react";
import { RoutingResult } from "./types";
import { QueryForm } from "./components/QueryForm";
import { ResultPanel } from "./components/ResultPanel";
import { MetricsDashboard } from "./components/MetricsDashboard";
import { AgentDiscovery } from "./components/AgentDiscovery";

type Tab = "query" | "metrics" | "agents";

const App: React.FC = () => {
  const [result, setResult] = useState<RoutingResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>("query");

  const handleSubmit = async (query: string) => {
    setLoading(true);
    setError(null);
    // Don't clear result immediately - keep it visible until new result arrives
    // This prevents the screen from disappearing

    try {
      const response = await fetch("/routing/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        const text = await response.text();
        let errorMessage = text || `Request failed with status ${response.status}`;
        
        // Try to parse as JSON if possible
        try {
          const errorJson = JSON.parse(text);
          errorMessage = errorJson.detail || errorJson.message || errorMessage;
        } catch {
          // Not JSON, use text as is
        }
        
        throw new Error(errorMessage);
      }

      const data = (await response.json()) as RoutingResult;
      setResult(data);
      setError(null); // Clear any previous errors on success
    } catch (err) {
      console.error("Routing error:", err);
      const errorMessage = err instanceof Error
        ? err.message
        : "Something went wrong while routing your query.";
      setError(errorMessage);
      // Don't clear result on error - keep previous result visible
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (tab: Tab) => {
    setActiveTab(tab);
  };

  return (
    <div className="app-root">
      <header className="app-header">
        <h1 className="app-title">
          <img
            src="/sagent-logo.png"
            alt="Sagent AI logo"
            className="app-logo-img"
          />
          <span className="app-title-text">agent AI</span>
        </h1>
        <p>
          Smart agentic routing powered by a knowledge graph –{" "}
          <strong>see which agent</strong> handled your query and{" "}
          <strong>why</strong>.
        </p>
      </header>

      <nav className="app-tabs">
        <button
          className={`tab-button ${activeTab === "query" ? "active" : ""}`}
          onClick={() => handleTabChange("query")}
        >
          Query Router
        </button>
        <button
          className={`tab-button ${activeTab === "agents" ? "active" : ""}`}
          onClick={() => handleTabChange("agents")}
        >
          Agent Discovery
        </button>
        <button
          className={`tab-button ${activeTab === "metrics" ? "active" : ""}`}
          onClick={() => handleTabChange("metrics")}
        >
          Metrics
        </button>
      </nav>

      <main className={`app-main ${activeTab === "query" ? "app-main--query" : ""}`}>
        {activeTab === "query" && (
          <>
            <section className="panel panel--query-form">
              <QueryForm onSubmit={handleSubmit} loading={loading} result={result} />
              {error && (
                <div className="error-banner" style={{ marginTop: "1rem" }}>
                  <strong>Error:</strong> {error}
                </div>
              )}
              {loading && !result && (
                <div style={{ marginTop: "1rem", textAlign: "center", color: "var(--text-muted)", padding: "1rem" }}>
                  Processing your query...
                </div>
              )}
            </section>

            {result && (
              <section className="panel panel--result">
                <ResultPanel result={result} />
              </section>
            )}
          </>
        )}

        {activeTab === "agents" && (
          <section className="panel panel--full-width">
            <AgentDiscovery />
          </section>
        )}

        {activeTab === "metrics" && (
          <section className="panel panel--full-width">
            <MetricsDashboard />
          </section>
        )}
      </main>

      <footer className="app-footer">
        <span>Backend: FastAPI + Neo4j + CrewAI | Frontend: React + Vite</span>
      </footer>
    </div>
  );
};

export default App;


