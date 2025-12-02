# Smart Agentic Router – Detailed Implementation Plan (Python + FastAPI + Neo4j)

This document is a step-by-step roadmap for implementing the **Smart Agentic Task Router** using:

- **Backend language:** Python  
- **Framework:** FastAPI  
- **Database / Knowledge Graph:** Neo4j (with Cypher)  

---

## PHASE 0 – Python Environment & Project Scaffolding (½–1 day)

### 0.1 Create project & virtual environment

```bash
mkdir smart_agentic_router
cd smart_agentic_router

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scriptsctivate

pip install fastapi uvicorn[standard] neo4j pydantic[dotenv] httpx
pip install black isort mypy pytest
```

(Optional) Use Poetry instead of raw pip.

### 0.2 Directory structure

```text
smart_agentic_router/
  backend/
    app.py
    config.py
    deps.py
    kg/
      client.py
      queries.py
      seed_data.cypher
      schema.cypher
    agents/
      query_analyzer.py
      kg_query_agent.py
      routing_decision_agent.py
      feedback_collector.py
      heuristics.py
    models/
      schemas.py
      domain.py
    api/
      routes/
        routing.py
        feedback.py
        agents.py
  tests/
    test_routing.py
  docs/
    graph_schema.md
    roadmap.md
```

### 0.3 Config management (FastAPI-friendly)

`backend/config.py`:

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    low_conf_threshold: float = 0.6

    class Config:
        env_file = ".env"

settings = Settings()
```

`.env`:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
LOW_CONF_THRESHOLD=0.6
```

---

## PHASE 1 – Neo4j Setup & Backend Connection (1 day)

### 1.1 Run Neo4j locally

Using Docker:

```bash
docker run   -e NEO4J_AUTH=neo4j/password   -p 7474:7474 -p 7687:7687   neo4j:5
```

Or via Neo4j Desktop (create DB with matching credentials).

### 1.2 Basic Neo4j connection wrapper

`backend/kg/client.py`:

```python
from neo4j import GraphDatabase
from ..config import settings

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
    return _driver

def close_driver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
```

### 1.3 Integrate with FastAPI lifecycle

`backend/deps.py`:

```python
from fastapi import Depends
from neo4j import Driver
from .kg.client import get_driver

def get_neo4j_driver() -> Driver:
    return get_driver()
```

`backend/app.py`:

```python
from fastapi import FastAPI
from .kg.client import get_driver, close_driver
from .api.routes import routing, feedback, agents

app = FastAPI(title="Smart Agentic Router")

@app.on_event("startup")
def on_startup():
    get_driver()  # initialize connection

@app.on_event("shutdown")
def on_shutdown():
    close_driver()

app.include_router(routing.router, prefix="/routing", tags=["routing"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
```

Run the app:

```bash
uvicorn backend.app:app --reload
```

---

## PHASE 2 – Graph Schema in Neo4j (1 day)

### 2.1 Decide labels & relationships

Document in `docs/graph_schema.md`:

- **Node labels:**
  - `:Agent`, `:SpecializedAgent`, `:RouterAgent`
  - `:TaskType`, `:Capability`, `:Query`, `:RoutingDecision`
- **Relationship types:**
  - `HAS_CAPABILITY`, `REQUIRES_CAPABILITY`  
  - `FALLBACK_AGENT`, `SIMILAR_TO`  
  - `SOURCE_QUERY`, `ROUTED_TO`, `SUCCESSFULLY_HANDLED`

### 2.2 Create constraints & indexes

`backend/kg/schema.cypher`:

```cypher
// Unique constraints
CREATE CONSTRAINT agent_name_unique IF NOT EXISTS
FOR (a:Agent)
REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT capability_name_unique IF NOT EXISTS
FOR (c:Capability)
REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT tasktype_name_unique IF NOT EXISTS
FOR (t:TaskType)
REQUIRE t.name IS UNIQUE;

// Indexes for faster lookup
CREATE INDEX query_text_index IF NOT EXISTS
FOR (q:Query)
ON (q.text);

CREATE INDEX routing_timestamp_index IF NOT EXISTS
FOR (rd:RoutingDecision)
ON (rd.timestamp);
```

Run this once via `cypher-shell` or a helper script.

---

## PHASE 3 – Design Sample Dataset (1 day)

### 3.1 Design the sample graph

In `docs/graph_schema.md`, add tables for:

- **Agents** (name, capabilityLevel, domain, fallback)
- **Capabilities**
- **Task types** and their required capabilities
- A few **sample queries** & routing outcomes

Example agents table:

| Agent name              | Level | Domain    | Capabilities                                | Fallback               |
|-------------------------|-------|-----------|---------------------------------------------|------------------------|
| WebSearchAgent          | 0.9   | general   | WebSearching, FactRetrieval                 | PerplexityFallback     |
| CodeAnalysisAgent       | 0.85  | technical | CodeUnderstanding, DebuggingAssistance      | PerplexityFallback     |
| SummarizationAgent      | 0.83  | general   | DocumentSummarization                       | WebSearchAgent         |
| DataVisualizationAgent  | 0.8   | technical | DataVisualization                           | SummarizationAgent     |
| PerplexityFallbackAgent | 0.8   | general   | GeneralKnowledge, WebSearching, FactRetrieval | (none)               |

Define TaskTypes like:

- `WebSearchTask` → `WebSearching`
- `CodeDebuggingTask` → `CodeUnderstanding`, `DebuggingAssistance`
- `SummarizationTask` → `DocumentSummarization`
- `VisualizationTask` → `DataVisualization`

---

## PHASE 4 – Seed Script for Neo4j (1–2 days)

### 4.1 Write `seed_data.cypher`

`backend/kg/seed_data.cypher` (shortened; expand with all data):

```cypher
// 1. Clean DB
MATCH (n) DETACH DELETE n;

// 2. Capabilities
CREATE (webCap:Capability {name: 'WebSearching'});
CREATE (factCap:Capability {name: 'FactRetrieval'});
CREATE (codeCap:Capability {name: 'CodeUnderstanding'});
CREATE (debugCap:Capability {name: 'DebuggingAssistance'});
CREATE (sumCap:Capability {name: 'DocumentSummarization'});
CREATE (vizCap:Capability {name: 'DataVisualization'});
CREATE (genCap:Capability {name: 'GeneralKnowledge'});

// 3. Agents
CREATE (web:SpecializedAgent:Agent {
  name: 'WebSearchAgent',
  capabilityLevel: 0.9,
  inputFormat: 'text',
  outputFormat: 'structured_results',
  domainExpertise: 'general'
});

// ... other agents ...

// 4. HAS_CAPABILITY relationships
MATCH (web:Agent {name: 'WebSearchAgent'})
MATCH (webCap:Capability {name: 'WebSearching'})
CREATE (web)-[:HAS_CAPABILITY]->(webCap);

MATCH (web),(factCap:Capability {name: 'FactRetrieval'})
CREATE (web)-[:HAS_CAPABILITY]->(factCap);

// etc for other agents/capabilities...

// 5. TaskTypes
CREATE (webTask:TaskType {name: 'WebSearchTask', complexityLevel: 0.3});
CREATE (codeDebugTask:TaskType {name: 'CodeDebuggingTask', complexityLevel: 0.8});

MATCH (webTask),(webCap) CREATE (webTask)-[:REQUIRES_CAPABILITY]->(webCap);
MATCH (codeDebugTask),(codeCap) CREATE (codeDebugTask)-[:REQUIRES_CAPABILITY]->(codeCap);
MATCH (codeDebugTask),(debugCap) CREATE (codeDebugTask)-[:REQUIRES_CAPABILITY]->(debugCap);

// 6. Fallbacks
MATCH (web:Agent {name:'WebSearchAgent'}),
      (perp:Agent {name:'PerplexityFallbackAgent'})
CREATE (web)-[:FALLBACK_AGENT]->(perp);

// 7. Sample RoutingDecision
CREATE (q1:Query {text: 'Find latest LLM pruning research'});
CREATE (rd1:RoutingDecision {timestamp: datetime(), confidence: 0.82, outcome: 'SUCCESS'});

MATCH (web),(q1)
CREATE (rd1)-[:SOURCE_QUERY]->(q1);
CREATE (rd1)-[:ROUTED_TO]->(web);
```

### 4.2 Helper script to run the seed

`backend/kg/seed.py`:

```python
from .client import get_driver

def run_seed_script():
    driver = get_driver()
    with open("backend/kg/seed_data.cypher") as f:
        cypher = f.read()
    with driver.session() as session:
        for stmt in cypher.split(";"):
            stmt = stmt.strip()
            if stmt:
                session.run(stmt)

if __name__ == "__main__":
    run_seed_script()
```

Run:

```bash
python -m backend.kg.seed
```

---

## PHASE 5 – KG Access Layer in Python (1–2 days)

### 5.1 Domain models

`backend/models/domain.py`:

```python
from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    capability_level: float
    domain_expertise: str
    input_format: str
    output_format: str

@dataclass
class RoutingDecision:
    id: str
    confidence: float
    outcome: str
```

### 5.2 Query helpers

`backend/kg/queries.py`:

```python
from typing import List
from neo4j import Session
from .client import get_driver
from ..models.domain import Agent

def _session() -> Session:
    return get_driver().session()

def get_agents_by_task_type(task_type_name: str) -> List[Agent]:
    cypher = """
    MATCH (tt:TaskType {name: $taskType})-[:REQUIRES_CAPABILITY]->(cap:Capability),
          (agent:Agent)-[:HAS_CAPABILITY]->(cap)
    WITH DISTINCT agent
    RETURN agent
    """
    with _session() as session:
        result = session.run(cypher, taskType=task_type_name)
        agents = []
        for record in result:
            node = record["agent"]
            agents.append(
                Agent(
                    name=node["name"],
                    capability_level=node.get("capabilityLevel", 0.5),
                    domain_expertise=node.get("domainExpertise", "general"),
                    input_format=node.get("inputFormat", "text"),
                    output_format=node.get("outputFormat", "text"),
                )
            )
        return agents

def get_fallback_agent(agent_name: str) -> Agent | None:
    cypher = """
    MATCH (a:Agent {name: $name})-[:FALLBACK_AGENT]->(fb:Agent)
    RETURN fb LIMIT 1
    """
    with _session() as session:
        record = session.run(cypher, name=agent_name).single()
        if not record:
            return None
        node = record["fb"]
        return Agent(
            name=node["name"],
            capability_level=node.get("capabilityLevel", 0.5),
            domain_expertise=node.get("domainExpertise", "general"),
            input_format=node.get("inputFormat", "text"),
            output_format=node.get("outputFormat", "text"),
        )

def create_routing_decision(query_text: str, agent_name: str, confidence: float) -> str:
    cypher = """
    MERGE (agent:Agent {name: $agentName})
    CREATE (q:Query {text: $queryText})
    CREATE (rd:RoutingDecision {
        id: randomUUID(),
        timestamp: datetime(),
        confidence: $confidence,
        outcome: 'PENDING'
    })
    CREATE (rd)-[:SOURCE_QUERY]->(q)
    CREATE (rd)-[:ROUTED_TO]->(agent)
    RETURN rd.id AS id
    """
    with _session() as session:
        record = session.run(
            cypher,
            agentName=agent_name,
            queryText=query_text,
            confidence=confidence,
        ).single()
        return record["id"]

def update_routing_outcome(rd_id: str, outcome: str):
    cypher = """
    MATCH (rd:RoutingDecision {id: $id})
    SET rd.outcome = $outcome
    """
    with _session() as session:
        session.run(cypher, id=rd_id, outcome=outcome)
```

You can later add `get_agent_stats()` and more.

---

## PHASE 6 – QueryAnalyzerAgent (2–3 days)

### 6.1 Pydantic schemas

`backend/models/schemas.py`:

```python
from pydantic import BaseModel

class RouteRequest(BaseModel):
    query: str

class AnalyzedQuery(BaseModel):
    raw_text: str
    task_type: str
    complexity: float
    domain: str
    output_format: str | None = None

class RoutingResult(BaseModel):
    routing_decision_id: str
    chosen_agent: str
    confidence: float
    rationale: dict
```

### 6.2 Simple heuristics-based QueryAnalyzer

`backend/agents/heuristics.py`:

```python
def infer_task_type(text: str) -> str:
    lower = text.lower()
    if "debug" in lower or "error" in lower or "stack trace" in lower:
        return "CodeDebuggingTask"
    if "summarize" in lower or "summary" in lower:
        return "SummarizationTask"
    if "plot" in lower or "graph" in lower or "chart" in lower:
        return "VisualizationTask"
    return "WebSearchTask"

def infer_complexity(text: str) -> float:
    lower = text.lower()
    if "simple" in lower:
        return 0.2
    if "complex" in lower or "advanced" in lower:
        return 0.8
    return 0.5

def infer_domain(text: str) -> str:
    lower = text.lower()
    if "python" in lower or "code" in lower or "bug" in lower:
        return "technical"
    if "contract" in lower or "legal" in lower:
        return "legal"
    return "general"

def infer_output_format(text: str) -> str | None:
    lower = text.lower()
    if "bullet" in lower or "bullets" in lower:
        return "bullet_summary"
    if "explain step by step" in lower:
        return "detailed_explanation"
    return None
```

`backend/agents/query_analyzer.py`:

```python
from . import heuristics
from ..models.schemas import AnalyzedQuery

def analyze_query(text: str) -> AnalyzedQuery:
    task_type = heuristics.infer_task_type(text)
    complexity = heuristics.infer_complexity(text)
    domain = heuristics.infer_domain(text)
    output_format = heuristics.infer_output_format(text)

    return AnalyzedQuery(
        raw_text=text,
        task_type=task_type,
        complexity=complexity,
        domain=domain,
        output_format=output_format,
    )
```

Later you can replace `heuristics` with GLiNER/LLM-based extraction.

---

## PHASE 7 – KGQueryAgent (2–3 days)

`backend/agents/kg_query_agent.py`:

```python
from typing import List, Tuple
from ..models.schemas import AnalyzedQuery
from ..models.domain import Agent
from ..kg.queries import get_agents_by_task_type

def score_agent(agent: Agent, analyzed: AnalyzedQuery, historical_score: float = 0.5) -> float:
    domain_match = 1.0 if agent.domain_expertise in (analyzed.domain, "general") else 0.7
    return 0.5 * agent.capability_level + 0.3 * historical_score + 0.2 * domain_match

def query_kg_for_agents(analyzed: AnalyzedQuery) -> List[Tuple[Agent, float]]:
    candidates = get_agents_by_task_type(analyzed.task_type)
    scored = [(agent, score_agent(agent, analyzed, 0.5)) for agent in candidates]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
```

---

## PHASE 8 – RoutingDecisionAgent (2–3 days)

`backend/agents/routing_decision_agent.py`:

```python
from ..models.schemas import RoutingResult
from ..config import settings
from .query_analyzer import analyze_query
from .kg_query_agent import query_kg_for_agents
from ..kg.queries import get_fallback_agent, create_routing_decision

def route_query(query: str) -> RoutingResult:
    analyzed = analyze_query(query)
    ranked = query_kg_for_agents(analyzed)

    if not ranked:
        chosen_name = "PerplexityFallbackAgent"
        confidence = 0.5
        candidates = []
    else:
        top_agent, top_score = ranked[0]
        chosen_name = top_agent.name
        confidence = top_score

        if confidence < settings.low_conf_threshold:
            fb = get_fallback_agent(chosen_name)
            if fb:
                chosen_name = fb.name

        candidates = [
            {"name": agent.name, "score": score}
            for agent, score in ranked[:3]
        ]

    rd_id = create_routing_decision(
        query_text=query,
        agent_name=chosen_name,
        confidence=confidence,
    )

    rationale = {
        "analyzed_query": analyzed.dict(),
        "top_candidates": candidates,
    }

    return RoutingResult(
        routing_decision_id=rd_id,
        chosen_agent=chosen_name,
        confidence=confidence,
        rationale=rationale,
    )
```

---

## PHASE 9 – FeedbackCollectorAgent (1–2 days)

`backend/models/schemas.py` (add):

```python
class FeedbackRequest(BaseModel):
    routing_decision_id: str
    success: bool
```

`backend/agents/feedback_collector.py`:

```python
from ..kg.queries import update_routing_outcome

def record_feedback(routing_decision_id: str, success: bool):
    outcome = "SUCCESS" if success else "FAILURE"
    update_routing_outcome(routing_decision_id, outcome)
    # Later: update per-agent performance stats here
```

---

## PHASE 10 – FastAPI Routes & End-to-End Wiring (3–5 days)

### 10.1 Routing API

`backend/api/routes/routing.py`:

```python
from fastapi import APIRouter
from ...models.schemas import RouteRequest, RoutingResult
from ...agents.routing_decision_agent import route_query

router = APIRouter()

@router.post("/", response_model=RoutingResult)
def route(route_request: RouteRequest):
    return route_query(route_request.query)
```

### 10.2 Feedback API

`backend/api/routes/feedback.py`:

```python
from fastapi import APIRouter
from ...models.schemas import FeedbackRequest
from ...agents.feedback_collector import record_feedback

router = APIRouter()

@router.post("/")
def submit_feedback(feedback: FeedbackRequest):
    record_feedback(feedback.routing_decision_id, feedback.success)
    return {"status": "ok"}
```

### 10.3 Agents listing API (debug/demo)

`backend/api/routes/agents.py`:

```python
from fastapi import APIRouter
from ...kg.queries import get_agents_by_task_type

router = APIRouter()

@router.get("/")
def list_agents(task_type: str | None = None):
    if not task_type:
        # TODO: implement list-all-agents query
        return []
    agents = get_agents_by_task_type(task_type)
    return [a.__dict__ for a in agents]
```

Now you can call:

- `POST /routing` with `{ "query": "debug this python error" }`
- `POST /feedback` with `{ "routing_decision_id": "...", "success": true }`

---

## PHASE 11 – Metrics, Edge Cases & Polish (2–3 days)

### 11.1 Agent metrics in Neo4j

Extend `seed_data.cypher` to include:

- `successCount`, `failureCount`, `historicalAccuracy` on each `Agent`.

Add in `kg/queries.py`:

```python
def update_agent_stats(agent_name: str, success: bool):
    cypher = """
    MATCH (a:Agent {name: $name})
    SET a.successCount = coalesce(a.successCount, 0) + CASE WHEN $success THEN 1 ELSE 0 END,
        a.failureCount = coalesce(a.failureCount, 0) + CASE WHEN $success THEN 0 ELSE 1 END,
        a.historicalAccuracy =
            toFloat(a.successCount) / (a.successCount + a.failureCount)
    """
    with _session() as session:
        session.run(cypher, name=agent_name, success=success)
```

Wire it into `record_feedback` so each feedback updates the agent stats, which you can then use in scoring.

### 11.2 Edge case handling

- Unknown task type → default to `WebSearchTask`, assign lower baseline confidence.
- No candidates returned → directly choose `PerplexityFallbackAgent` and log this.
- Neo4j issues → catch exceptions, return HTTP 503 with message.

### 11.3 Logging

Add logging in critical paths (routing & feedback).

```python
import logging
logger = logging.getLogger(__name__)
```

Example in `route_query`:

```python
logger.info("Routing query='%s' to agent='%s' conf=%.2f", query, chosen_name, confidence)
```

---

## PHASE 12 – Timeline Summary (Approximate 4-Week Plan)

### Week 1
- Python/FastAPI skeleton
- Neo4j local instance up
- `client.py`, `schema.cypher`, `seed_data.cypher`
- Seed and verify graph in Neo4j Browser

### Week 2
- Implement `domain.py`, `schemas.py`
- `kg/queries.py` core helpers
- `QueryAnalyzerAgent` (heuristics)
- `KGQueryAgent` scoring v1

### Week 3
- `RoutingDecisionAgent` end-to-end routing
- `FeedbackCollectorAgent` and outcome updates
- FastAPI routes: `/routing`, `/feedback`, `/agents`
- Manual testing using curl/Postman/Swagger UI

### Week 4
- Add historicalAccuracy metrics and integrate into scoring
- Handle edge cases and add logging
- Optional simple frontend or just use Swagger UI for demo
- Prepare a demo script with 3–4 polished example flows showing routing + feedback + improvement

---

This markdown file is your implementation playbook.  
You can tweak details (e.g., names, scoring weights, capabilities), but the structure is solid enough to carry you from zero to a working Smart Agentic Router prototype.
