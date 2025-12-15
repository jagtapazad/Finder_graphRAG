# Setup Scripts

This folder contains utility scripts for database maintenance.

## Core Setup

**First-time setup** - Run this to initialize the database:

```bash
python backend/kg/seed.py
```

This will:
1. Apply schema constraints and indexes (`schema.cypher`)
2. Load 30 agents with capabilities and relationships (`seed_data.cypher`)

## Database Maintenance

**Clear all data** (use with caution):
```bash
python setup/clear_neo4j.py
```

## What Gets Loaded

- **30 Agents**: Diverse agents covering web search, code analysis, document processing, data analytics, content creation, communication, and specialized domains
- **Capabilities**: 30+ capabilities linked to agents
- **TaskTypes**: 5 core task types (WebSearchTask, CodeDebuggingTask, SummarizationTask, VisualizationTask, OtherTask)
- **Relationships**: FALLBACK_AGENT, SIMILAR_TO, COMPLEMENTS, WORKS_WITH, HAS_CAPABILITY, REQUIRES_CAPABILITY

## Verification

After running the seed script, verify in Neo4j Browser:

```cypher
MATCH (a:Agent) RETURN count(a) as agent_count;
MATCH (t:TaskType) RETURN count(t) as task_type_count;
MATCH ()-[r]->() RETURN type(r) as rel_type, count(*) as count ORDER BY count DESC;
```
