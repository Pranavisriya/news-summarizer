from tavily import TavilyClient #type: ignore
import os
from state import AgentState


def search_web(state: AgentState):
    """
    Node 1: Intelligent Web Search

    Uses Tavily's AI-optimized search to find and process web information.
    Behind the scenes: Tavily searches multiple sources, extracts relevant content,
    and uses AI to synthesize the information into a coherent answer.
    """
    #print(f"🔍 Searching: {state['question']}")
    client = TavilyClient(os.getenv("TAVILY_API_KEY"))


    search_results = client.search(
        query=state["question"],
        max_results=3,           # Number of sources to aggregate
        include_answer=True      # Get AI-generated answer, not just links!
    )

    return {"search_results": search_results}
