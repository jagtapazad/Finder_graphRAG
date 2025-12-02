import React, { useState } from "react";

type Props = {
  onSubmit: (query: string) => void | Promise<void>;
  loading: boolean;
};

export const QueryForm: React.FC<Props> = ({ onSubmit, loading }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    onSubmit(query.trim());
  };

  return (
    <form className="query-form" onSubmit={handleSubmit}>
      <label className="label">
        Enter your task or question
        <textarea
          className="textarea"
          placeholder="e.g., Debug this Python function that keeps timing out..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={4}
        />
      </label>
      <div className="query-form-footer">
        <button className="primary-btn" type="submit" disabled={loading}>
          {loading ? "Routing..." : "Route to best agent"}
        </button>
        <span className="hint">
          The router will analyze your query, traverse the knowledge graph, and
          explain why it chose a specific agent.
        </span>
      </div>
    </form>
  );
};


