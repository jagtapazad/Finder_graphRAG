import React, { useEffect, useState } from "react";

type Agent = {
  name: string;
  capability_level: number;
  domain_expertise: string;
  input_format: string;
  output_format: string;
  historical_accuracy: number;
  response_time: number;
  cost_efficiency: number;
  reliability: number;
  specialization_score: number;
  description?: string;
  success_count: number;
  failure_count: number;
  capabilities?: string[];
  keywords?: string[];
  query_patterns?: string[];
  use_cases?: string[];
  tags?: string[];
  tag_categories?: {
    industry?: string[];
    domain?: string[];
    capability?: string[];
    purpose?: string[];
  };
};

export const AgentDiscovery: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterDomain, setFilterDomain] = useState<string>("all");
  const [sortBy, setSortBy] = useState<string>("name");

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    setLoading(true);
    try {
      const response = await fetch("/agents/");
      if (!response.ok) {
        throw new Error("Failed to fetch agents");
      }
      const data = await response.json();
      setAgents(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load agents");
    } finally {
      setLoading(false);
    }
  };


  const filteredAndSortedAgents = agents
    .filter((agent) => {
      const matchesSearch =
        agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        agent.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        agent.domain_expertise.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesDomain = filterDomain === "all" || agent.domain_expertise === filterDomain;
      return matchesSearch && matchesDomain;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case "name":
          return a.name.localeCompare(b.name);
        case "capability":
          return b.capability_level - a.capability_level;
        case "accuracy":
          return b.historical_accuracy - a.historical_accuracy;
        case "reliability":
          return b.reliability - a.reliability;
        default:
          return 0;
      }
    });

  const domains = Array.from(new Set(agents.map((a) => a.domain_expertise))).sort();

  if (loading) {
    return (
      <div className="agent-discovery">
        <h3>Agent Discovery</h3>
        <p className="muted">Loading agents...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="agent-discovery">
        <h3>Agent Discovery</h3>
        <div className="error-banner">{error}</div>
      </div>
    );
  }

  return (
    <div className="agent-discovery">
      <h3>Agent Discovery</h3>
      <p className="muted">
        Explore all {agents.length} available agents and their capabilities
      </p>

      <div className="discovery-filters">
        <div className="filter-group">
          <label htmlFor="search">Search:</label>
          <input
            id="search"
            type="text"
            placeholder="Search by name, description, or domain..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="filter-input"
          />
        </div>
        <div className="filter-group">
          <label htmlFor="domain">Domain:</label>
          <select
            id="domain"
            value={filterDomain}
            onChange={(e) => setFilterDomain(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Domains</option>
            {domains.map((domain) => (
              <option key={domain} value={domain}>
                {domain}
              </option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <label htmlFor="sort">Sort by:</label>
          <select
            id="sort"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="filter-select"
          >
            <option value="name">Name</option>
            <option value="capability">Capability Level</option>
            <option value="accuracy">Historical Accuracy</option>
            <option value="reliability">Reliability</option>
          </select>
        </div>
      </div>

      <div className="agents-grid">
        {filteredAndSortedAgents.length === 0 ? (
          <p className="muted">No agents found matching your criteria.</p>
        ) : (
          filteredAndSortedAgents.map((agent) => (
            <AgentCard key={agent.name} agent={agent} />
          ))
        )}
      </div>
    </div>
  );
};

type AgentCardProps = {
  agent: Agent;
};

const AgentCard: React.FC<AgentCardProps> = ({ agent }) => {
  const [expanded, setExpanded] = useState(false);
  const [capabilities, setCapabilities] = useState<string[]>(agent.capabilities || []);
  const [tagCategories, setTagCategories] = useState<{
    industry?: string[];
    domain?: string[];
    capability?: string[];
    purpose?: string[];
  }>(agent.tag_categories || {});

  const handleExpand = async () => {
    if (!expanded && (capabilities.length === 0 || !agent.tag_categories)) {
      // Fetch capabilities and tags on first expand
      try {
        const response = await fetch(`/agents/${encodeURIComponent(agent.name)}`);
        if (response.ok) {
          const data = await response.json();
          setCapabilities(data.capabilities || []);
          setTagCategories(data.tag_categories || {});
        }
      } catch (err) {
        console.error(`Failed to fetch capabilities for ${agent.name}:`, err);
      }
    }
    setExpanded(!expanded);
  };

  return (
    <div className="agent-card">
      <div className="agent-card-header">
        <h4>{agent.name}</h4>
        <span className={`agent-badge agent-badge--${agent.domain_expertise}`}>
          {agent.domain_expertise}
        </span>
      </div>

      <p className="agent-description">{agent.description || "No description available."}</p>

      <div className="agent-metrics">
        <div className="metric-item">
          <span className="metric-label">Capability</span>
          <span className="metric-value">
            {(agent.capability_level * 100).toFixed(0)}%
          </span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Accuracy</span>
          <span className="metric-value">
            {(agent.historical_accuracy * 100).toFixed(0)}%
          </span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Reliability</span>
          <span className="metric-value">
            {(agent.reliability * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      <div className="agent-details">
        <div className="detail-row">
          <span className="detail-label">Input:</span>
          <span className="detail-value">{agent.input_format}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Output:</span>
          <span className="detail-value">{agent.output_format}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Response Time:</span>
          <span className="detail-value">
            {(agent.response_time * 100).toFixed(0)}ms
          </span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Cost Efficiency:</span>
          <span className="detail-value">
            {(agent.cost_efficiency * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      {agent.success_count + agent.failure_count > 0 && (
        <div className="agent-stats">
          <span className="stat-item">
            ✓ {agent.success_count} successes
          </span>
          <span className="stat-item">
            ✗ {agent.failure_count} failures
          </span>
        </div>
      )}

      <button
        className="expand-button"
        onClick={handleExpand}
      >
        {expanded ? "Hide" : "Show"} Capabilities
      </button>

      {expanded && (
        <div className="agent-capabilities">
          {/* Capabilities Section */}
          {capabilities.length > 0 && (
            <div className="capability-section">
              <h5 className="section-title">Capabilities</h5>
              <div className="tags-container">
                {capabilities.map((cap, idx) => (
                  <span key={idx} className="capability-tag">
                    {cap}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Tags Section - Organized by Category */}
          {(tagCategories.industry?.length || 
            tagCategories.domain?.length || 
            tagCategories.capability?.length || 
            tagCategories.purpose?.length) && (
            <div className="tags-section">
              <h5 className="section-title">Tags</h5>
              
              {tagCategories.industry && tagCategories.industry.length > 0 && (
                <div className="tag-category">
                  <span className="tag-category-label">Industry:</span>
                  <div className="tags-container">
                    {tagCategories.industry.map((tag, idx) => (
                      <span key={idx} className="tag tag--industry">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {tagCategories.domain && tagCategories.domain.length > 0 && (
                <div className="tag-category">
                  <span className="tag-category-label">Domain:</span>
                  <div className="tags-container">
                    {tagCategories.domain.map((tag, idx) => (
                      <span key={idx} className="tag tag--domain">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {tagCategories.capability && tagCategories.capability.length > 0 && (
                <div className="tag-category">
                  <span className="tag-category-label">Capability:</span>
                  <div className="tags-container">
                    {tagCategories.capability.map((tag, idx) => (
                      <span key={idx} className="tag tag--capability">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {tagCategories.purpose && tagCategories.purpose.length > 0 && (
                <div className="tag-category">
                  <span className="tag-category-label">Purpose:</span>
                  <div className="tags-container">
                    {tagCategories.purpose.map((tag, idx) => (
                      <span key={idx} className="tag tag--purpose">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {capabilities.length === 0 && 
           !tagCategories.industry?.length && 
           !tagCategories.domain?.length && 
           !tagCategories.capability?.length && 
           !tagCategories.purpose?.length && (
            <p className="muted small">Loading capabilities and tags...</p>
          )}
        </div>
      )}
    </div>
  );
};

