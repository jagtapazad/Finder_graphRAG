import React from "react";

type WorkflowStep = {
  id: string;
  label: string;
  description: string;
  icon: string;
};

const workflowSteps: WorkflowStep[] = [
  {
    id: "1",
    label: "User Query",
    description: "Input received",
    icon: "📥",
  },
  {
    id: "2",
    label: "LLM Extraction",
    description: "QueryAnalyzer Agent",
    icon: "🔍",
  },
  {
    id: "3",
    label: "KG Query",
    description: "KnowledgeGraphQuerier",
    icon: "🕸️",
  },
  {
    id: "4",
    label: "Agent Scoring",
    description: "RoutingDecisionMaker",
    icon: "⚖️",
  },
  {
    id: "5",
    label: "Routing Decision",
    description: "Agent selected",
    icon: "✅",
  },
  {
    id: "6",
    label: "Feedback Loop",
    description: "Learning & improvement",
    icon: "🔄",
  },
];

export const WorkflowTile: React.FC = () => {
  return (
    <div className="result-tile result-tile--workflow">
      <h3 className="result-tile-title">End-to-End Workflow</h3>
      <div className="workflow-container">
        {workflowSteps.map((step, index) => (
          <React.Fragment key={step.id}>
            <div className="workflow-step">
              <div className="workflow-step-icon">{step.icon}</div>
              <div className="workflow-step-content">
                <div className="workflow-step-number">{step.id}</div>
                <div className="workflow-step-label">{step.label}</div>
                <div className="workflow-step-description">{step.description}</div>
              </div>
            </div>
            {index < workflowSteps.length - 1 && (
              <div className="workflow-arrow">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M7 5L13 10L7 15"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};



