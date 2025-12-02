## Smart Agentic Router – Finder GraphRAG

This project implements the **Smart Agentic Task Router** described in your updated proposal and detailed implementation plan using:

- **FastAPI** for the backend API
- **Neo4j** as the knowledge graph (Graph RAG)
- **CrewAI** for multi-agent orchestration
- **LLM-based extraction** for query understanding

The design follows the phases and components outlined in:

- Updated proposal (`Doc_Folder/Smart Agentic Router Proposal Updated.pdf`)
- Detailed plan (`Doc_Folder/smart_agentic_router_full_plan_llm_crewai.txt`)

### High-level architecture

- `backend/app.py` – FastAPI app wiring and lifecycle
- `backend/config.py` – configuration and environment variables
- `backend/kg/` – Neo4j driver, schema, seed data, and Cypher helpers
- `backend/extraction/` – LLM-based query analyzer (prompt + parser)
- `backend/models/` – Pydantic API schemas and internal domain models
- `backend/agents/` – KG query & feedback logic
- `backend/crew/` – CrewAI agent definitions and routing flow
- `backend/api/routes/` – HTTP endpoints for routing, feedback, and agent listing

### Quick start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up a local Neo4j instance and update `.env` with your credentials and LLM API key.
4. Apply Neo4j schema (`backend/kg/schema.cypher`) and seed data (`backend/kg/seed_data.cypher` via `backend/kg/seed.py`).
5. Run the API:

```bash
uvicorn backend.app:app --reload
```


