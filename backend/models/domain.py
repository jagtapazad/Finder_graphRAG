from dataclasses import dataclass


@dataclass
class Agent:
    name: str
    capability_level: float
    domain_expertise: str
    input_format: str
    output_format: str
    historical_accuracy: float = 0.5
    response_time: float = 1.0  # Average response time (lower is better, normalized 0-1)
    cost_efficiency: float = 0.5  # Cost efficiency score (0-1, higher is better)
    reliability: float = 0.5  # Reliability score (0-1, higher is better)
    specialization_score: float = 0.5  # How specialized this agent is for the task (0-1)
    description: str = ""  # Agent description


@dataclass
class RoutingDecision:
    id: str
    confidence: float
    outcome: str


