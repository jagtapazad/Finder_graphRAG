import React, { useState } from "react";
import { RoutingResult } from "./types";
import { QueryForm } from "./components/QueryForm";
import { ResultPanel } from "./components/ResultPanel";

const App: React.FC = () => {
  const [result, setResult] = useState<RoutingResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (query: string) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("/routing/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Request failed with status ${response.status}`);
      }

      const data = (await response.json()) as RoutingResult;
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while routing your query."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-root">
      <header className="app-header">
        <h1>Smart Agentic Router</h1>
        <p>
          Understand <strong>which agent</strong> handled your query and{" "}
          <strong>why</strong>, with a clear view into the knowledge graph
          reasoning.
        </p>
      </header>

      <main className="app-main">
        <section className="panel">
          <QueryForm onSubmit={handleSubmit} loading={loading} />
          {error && <div className="error-banner">{error}</div>}
        </section>

        {result && (
          <section className="panel">
            <ResultPanel result={result} />
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


