import os
from crewai import Agent, LLM
from ..config import settings

if settings.llm_api_key:
    os.environ["GOOGLE_API_KEY"] = settings.llm_api_key

def get_gemini_llm():
    try:
        model = settings.llm_model if settings.llm_model else "gemini-2.0-flash"
        model_name = f"gemini/{model}"
        return LLM(model=model_name)
    except Exception as e:
        return LLM(model="gemini/gemini-2.0-flash")

_gemini_llm = None

def get_llm():
    global _gemini_llm
    if _gemini_llm is None:
        _gemini_llm = get_gemini_llm()
    return _gemini_llm

extractor_agent = Agent(
    role="QueryAnalyzer",
    goal="Parse user query into structured task metadata",
    backstory="You specialize in understanding user intents and mapping them to task types using LLM extraction. You analyze queries to extract task_type, complexity, domain, and output format requirements.",
    llm=get_llm(),
    verbose=True,
)

kg_query_agent = Agent(
    role="KnowledgeGraphQuerier",
    goal="Query the knowledge graph to find suitable agents",
    backstory="You know how to construct and execute Cypher queries against Neo4j to find agents matching task requirements. You understand the graph structure: TaskType -> Capabilities -> Agents.",
    llm=get_llm(),
    verbose=True,
)

router_agent = Agent(
    role="RoutingDecisionMaker",
    goal="Select the optimal specialized agent and decide fallback if needed",
    backstory="You consider capabilities, domain fit, historical performance, and confidence scores to make routing decisions. You apply tie-breaking logic when multiple agents have similar scores.",
    llm=get_llm(),
    verbose=True,
)

web_search_agent = Agent(
    role="WebSearchAgent",
    goal="Handle information retrieval and web search queries",
    backstory="You are an expert at finding and retrieving information from the web.",
    llm=get_llm(),
    verbose=True,
)

code_analysis_agent = Agent(
    role="CodeAnalysisAgent",
    goal="Analyze and debug code-related tasks",
    backstory="You specialize in understanding, analyzing, and debugging code across multiple programming languages.",
    llm=get_llm(),
    verbose=True,
)

summarization_agent = Agent(
    role="SummarizationAgent",
    goal="Summarize documents and text",
    backstory="You excel at condensing long documents and texts into concise, informative summaries.",
    llm=get_llm(),
    verbose=True,
)

fallback_agent = Agent(
    role="FallbackAgent",
    goal="Provide a reasonable generic answer when no specialized agent fits",
    backstory="You are a general-purpose assistant that handles queries when no specialized agent is available.",
    llm=get_llm(),
    verbose=True,
)

feedback_agent = Agent(
    role="FeedbackCollector",
    goal="Collect user feedback and update agent performance stats in the KG",
    backstory="You track and analyze routing outcomes to improve the system's performance over time. You update agent historical accuracy, success/failure counts, and routing decision outcomes in Neo4j.",
    llm=get_llm(),
    verbose=True,
)


