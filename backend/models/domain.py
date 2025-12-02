from dataclasses import dataclass


@dataclass
class Agent:
    name: str
    capability_level: float
    domain_expertise: str
    input_format: str
    output_format: str
    historical_accuracy: float = 0.5


@dataclass
class RoutingDecision:
    id: str
    confidence: float
    outcome: str


