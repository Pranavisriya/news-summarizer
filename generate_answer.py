from state import AgentState

def generate_answer(state: AgentState):
    """
    Node 2: Answer Synthesis and Formatting

    Takes the search results from Tavily and formats them into a clean,
    user-friendly response with proper source attribution.
    """
    #print("🤖 Formatting answer...")

    # Extract Tavily's AI-generated answer (the smart synthesis)
    ai_answer = state["search_results"].get("answer", "No answer found")

    # Extract source URLs for transparency and verification
    sources = [f"- {result['title']}: {result['url']}" 
              for result in state["search_results"]["results"]]

    # Combine the intelligent answer with source attribution
    final_answer = f"{ai_answer}\n\nSources:\n" + "\n".join(sources)

    return {"answer": final_answer}