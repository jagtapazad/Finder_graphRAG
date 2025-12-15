# Smart Agentic Router – Finder GraphRAG

An intelligent multi-agent system that routes user queries to specialized AI agents using a Neo4j knowledge graph (Graph RAG) and CrewAI orchestration. The system learns from feedback to improve routing decisions over time.

## Key Features

- ✅ **4-Agent Architecture**: QueryAnalyzer → KG Query → RoutingDecision → FeedbackCollector
- ✅ **Explainable Routing**: Graph traversal path showing why an agent was chosen
- ✅ **Knowledge Graph Integration**: Neo4j with Cypher queries for agent discovery
- ✅ **Learning from Feedback**: Historical accuracy updates improve future routing
- ✅ **31+ Specialized Agents**: Comprehensive agent catalog covering multiple domains
- ✅ **Edge Case Handling**: Fallback agents, tie-breaking, low confidence scenarios
- ✅ **Interactive UI**: React frontend with graph visualization and metrics dashboard

## Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Knowledge Graph**: Neo4j Aura (cloud) with Cypher queries
- **LLM**: Google Gemini 2.0 Flash (`google-generativeai` SDK)
- **Agent Framework**: CrewAI
- **Frontend**: React + TypeScript + Vite
- **Authentication**: Neo4j OAuth (for Aura cloud instances)

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Neo4j Aura instance (or local Neo4j)

### Installation

1. **Clone repository**:
   ```bash
   git clone https://github.com/jagtapazad/Finder_graphRAG.git
   cd Finder_graphRAG
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create `.env` file in project root:
   ```env
   NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
   NEO4J_CLIENT_ID=your_client_id
   NEO4J_CLIENT_SECRET=your_client_secret
   LLM_API_KEY=your_gemini_api_key
   LLM_MODEL=gemini-2.0-flash
   GOOGLE_API_KEY=your_gemini_api_key
   LOW_CONF_THRESHOLD=0.6
   ```

5. **Seed the knowledge graph**:
   ```bash
   python backend/kg/seed.py
   ```

6. **Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

**Terminal 1 - Backend**:
```bash
source .venv/bin/activate
export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Access**:
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs
- Backend API: http://localhost:8000

## Architecture

### System Overview

```
┌─────────────┐
│   Frontend  │ (React + Vite)
│  (React UI) │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐
│   Backend   │ (FastAPI)
│   API Layer │
└──────┬──────┘
       │
       ├──► Extraction (LLM)
       ├──► Agent Orchestration (CrewAI)
       └──► Knowledge Graph (Neo4j)
```

### 4-Agent Architecture

1. **QueryAnalyzer Agent**: Extracts task metadata (task_type, domain, complexity) from user queries using Google Gemini LLM
2. **KnowledgeGraph Query Agent**: Queries Neo4j to find candidate agents matching task requirements
3. **RoutingDecision Agent**: Scores candidates using multi-axis algorithm and selects optimal agent
4. **FeedbackCollector Agent**: Updates agent performance metrics from user feedback

### Knowledge Graph Schema

**Node Types**:
- `Agent`: Specialized agents with capabilities and performance metrics
- `Capability`: Skills/abilities that agents possess
- `TaskType`: Types of tasks requiring specific capabilities
- `Query`: User queries
- `RoutingDecision`: Routing decisions with outcomes

**Relationships**:
- `Agent -[:HAS_CAPABILITY]-> Capability`
- `TaskType -[:REQUIRES_CAPABILITY]-> Capability`
- `Agent -[:FALLBACK_AGENT]-> Agent`
- `RoutingDecision -[:SOURCE_QUERY]-> Query`
- `RoutingDecision -[:ROUTED_TO]-> Agent`

### Routing Flow

```
User Query 
  → QueryAnalyzer Agent (LLM extraction, ~800ms)
  → KGQuerier Agent (Neo4j query, ~50ms)
  → Router Agent (scoring & selection, ~10ms)
  → Create RoutingDecision in Neo4j
  → Return Result
  → [Asynchronous] User Feedback
  → FeedbackCollector Agent (update KG, ~20ms)
```

**Total Routing Time**: ~860ms average

### Scoring Algorithm

7-factor weighted scoring system:
- Capability level: 25%
- Historical accuracy: 20%
- Domain match: 25%
- Response time: 10%
- Cost efficiency: 10%
- Reliability: 5%
- Specialization score: 5%

## API Endpoints

- `POST /routing/` - Route a user query
- `GET /explanations/routing/{rd_id}/explanation` - Get routing explanation
- `GET /explanations/routing/{rd_id}/path` - Get routing path
- `POST /feedback/` - Submit feedback for routing decision
- `GET /visualization/kg/visualization` - Get KG data for visualization
- `GET /metrics/` - Get routing metrics dashboard
- `GET /agents/` - List all agents (optional `?task_type={type}` filter)
- `GET /agents/{agent_name}` - Get agent details

## Project Structure

```
Finder_graphRAG/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── config.py              # Configuration & settings
│   ├── api/routes/            # API endpoints
│   ├── agents/                # Agent logic (KG query, feedback)
│   ├── crew/                  # CrewAI agent definitions
│   ├── extraction/            # LLM query extraction
│   ├── kg/                    # Neo4j queries & schema
│   └── models/                # Pydantic schemas & domain models
├── frontend/
│   └── src/                   # React application
├── setup/                     # One-time setup scripts
│   ├── cypher/                # Additional Cypher seed files
│   └── *.py                   # Setup utility scripts
├── artifacts/                 # RDF/SHACL/OWL semantic artifacts
└── requirements.txt           # Python dependencies
```

## Key Components

### Backend

- **`backend/app.py`** - FastAPI application with route registration
- **`backend/config.py`** - Configuration and environment variables
- **`backend/kg/`** - Neo4j integration:
  - `key_queries.py` - 6 documented Cypher queries
  - `queries.py` - Query functions
  - `schema.cypher` - Database schema
  - `seed_data.cypher` - Core seed data
  - `seed.py` - Python seeding script
- **`backend/extraction/`** - LLM query extraction:
  - `llm_extractor.py` - Gemini integration
  - `prompt_templates.py` - Extraction prompts
- **`backend/crew/`** - CrewAI agents:
  - `agents.py` - Agent definitions
  - `crew_config.py` - Routing flow orchestration
- **`backend/api/routes/`** - API endpoints

### Frontend

- **`frontend/src/App.tsx`** - Main application
- **`frontend/src/components/`**:
  - `QueryForm.tsx` - Query input form
  - `ResultPanel.tsx` - Routing results with explanation
  - `TraversalTimeline.tsx` - Graph traversal visualization
  - `KGVisualization.tsx` - Knowledge graph visualization
  - `MetricsDashboard.tsx` - Performance metrics
  - `AgentDiscovery.tsx` - Agent browsing interface

## Demo Scenarios

### Scenario 1: Web Search Query

**Query**: "Find latest LLM pruning research"

**Flow**:
1. Extracted: `task_type: "WebSearchTask"`, `domain: "research"`, `complexity: 0.7`
2. Found agents: WebSearchAgent, ResearchAssistant, DeepSearch Agent
3. Selected: ResearchAssistant (score: 0.848)
4. Confidence: 84.8%

### Scenario 2: Code Debugging Query

**Query**: "Fix Python syntax error in my code"

**Flow**:
1. Extracted: `task_type: "CodeDebuggingTask"`, `domain: "technical"`, `complexity: 0.8`
2. Found agents: CodeAnalysisAgent, DebugMaster, CodeAnalyzer Pro
3. Selected: CodeAnalysisAgent (score: 0.88)
4. Confidence: 88%

### Scenario 3: Document Summarization

**Query**: "Summarize this long document"

**Flow**:
1. Extracted: `task_type: "SummarizationTask"`, `domain: "general"`, `complexity: 0.5`
2. Found agents: SummarizationAgent, DocumentSummarizer
3. Selected: SummarizationAgent (score: 0.78)
4. Confidence: 78%

## Setup Scripts

One-time setup scripts are located in `setup/` folder:

- **`setup/cypher/`** - Additional Cypher seed files for extended agent catalogs
- **`setup/*.py`** - Utility scripts for database setup and maintenance

See `setup/README.md` for detailed setup instructions.

## Configuration

Environment variables (`.env`):
- `NEO4J_URI`: Neo4j connection URI (e.g., `neo4j+s://instance.databases.neo4j.io`)
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `NEO4J_CLIENT_ID`: OAuth client ID (for Aura)
- `NEO4J_CLIENT_SECRET`: OAuth client secret (for Aura)
- `LLM_API_KEY`: Google Gemini API key
- `LLM_MODEL`: Model name (default: "gemini-2.0-flash")
- `GOOGLE_API_KEY`: Google API key (for CrewAI)
- `LOW_CONF_THRESHOLD`: Confidence threshold for fallback (default: 0.6)

## Key Cypher Queries

See `backend/kg/key_queries.py` for documented queries:

1. **Query 1**: Find agents by task type with capability threshold
2. **Query 2**: Find similar agents for fallback scenarios
3. **Query 3**: Retrieve historical routing decisions
4. **Query 4**: Find agents by domain expertise
5. **Query 5**: Get routing path explanation
6. **Query 6**: Get full graph traversal path

## Edge Cases

1. **No agents match**: Falls back to `PerplexityFallbackAgent`
2. **Low confidence (< 0.6)**: Checks for fallback agent relationship
3. **Tie scores**: Uses tie-breaking criteria (capability level, historical accuracy, domain match)
4. **New task type**: Routes to general agents or fallback
5. **LLM extraction failure**: Uses default values (WebSearchTask, complexity 0.5, domain "general")

## Performance Metrics

- **Average Routing Time**: ~860ms (LLM extraction: ~800ms, KG query: ~50ms, scoring: ~10ms)
- **Neo4j Query Performance**: <50ms average for typical queries
- **LLM Extraction Accuracy**: >90% for common query types
- **Domain Classification Accuracy**: ~85% (measured on 100 test queries)

## Troubleshooting

### Backend Issues

**Neo4j Connection Errors**:
- Verify `.env` file has correct credentials
- Check Neo4j Aura instance is running
- Ensure SSL certificates are properly configured (use `certifi`)

**LLM Extraction Errors**:
- Verify `LLM_API_KEY` is set correctly
- Check API key is valid and has quota
- Review error logs for specific Gemini API errors

### Frontend Issues

**Proxy Errors**:
- Ensure backend is running on port 8000
- Check `vite.config.mts` proxy configuration
- Verify CORS settings in `backend/app.py`

## License

[Your License Here]

## Repository

**GitHub**: https://github.com/jagtapazad/Finder_graphRAG
