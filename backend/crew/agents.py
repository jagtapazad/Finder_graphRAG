import os
from crewai import Agent, LLM
from ..config import settings

# Set GOOGLE_API_KEY environment variable for CrewAI (required)
if settings.llm_api_key:
    os.environ["GOOGLE_API_KEY"] = settings.llm_api_key

# Configure Gemini LLM for all agents (lazy initialization to avoid blocking startup)
# CrewAI Gemini model format: "gemini/gemini-1.5-flash" or "gemini/gemini-1.5-pro"
def get_gemini_llm():
    """Lazy initialization of Gemini LLM to avoid blocking server startup"""
    try:
        model_name = f"gemini/{settings.llm_model}" if settings.llm_model else "gemini/gemini-1.5-flash"
        return LLM(model=model_name)
    except Exception as e:
        # Fallback: use default Gemini model
        return LLM(model="gemini/gemini-1.5-flash")

_gemini_llm = None

def get_llm():
    global _gemini_llm
    if _gemini_llm is None:
        _gemini_llm = get_gemini_llm()
    return _gemini_llm

extractor_agent = Agent(
    role="Extractor",
    goal="Parse user query into structured task metadata",
    backstory="You specialize in understanding user intents and mapping them to task types.",
    llm=get_llm(),
    verbose=True,
)

kg_query_agent = Agent(
    role="KGQuerier",
    goal="Query the knowledge graph to find suitable agents",
    backstory="You know how to interact with Neo4j and read agent capabilities.",
    llm=get_llm(),
    verbose=True,
)

router_agent = Agent(
    role="Router",
    goal="Select the optimal specialized agent and decide fallback if needed",
    backstory="You consider capabilities, domain fit, and historical performance.",
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
    backstory="You track and analyze routing outcomes to improve the system's performance over time.",
    llm=get_llm(),
    verbose=True,
)


