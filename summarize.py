from state import AgentState, NewsSummary
from langchain_openai import ChatOpenAI # type: ignore
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

OPEN_API_KEY= os.getenv("OPEN_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",     
    temperature=0.0,
    api_key=OPEN_API_KEY
)

def summarize_answer(state: AgentState):
    """
    Node 3: Final Summary Refinement

    Further refines the generated answer for clarity, conciseness, and readability.
    """
    formatted_answer = state.get("answer", "").strip()
    results = (state.get("search_results") or {}).get("results", []) or []

    docs = []
    for r in results[:5]:
        title = r.get("title", "Untitled")
        url = r.get("url", "")
        content = r.get("content") or r.get("snippet") or ""
        docs.append(f"Title: {title}\nURL: {url}\nContent:\n{content}")
    corpus = "\n\n---\n\n".join(docs)

    prompt = f"""
You are a factual news summarizer. Write a concise, neutral, 6–10 sentence summary
for the user's question below using the provided source extracts AND the formatted answer.
Lead with what/when/where (use concrete dates if present), include key developments and
any official statements, avoid speculation, and flag disputed points. End with a short
'Sources:' list of only links of sources.

User question: {state.get('question', '')}

Formatted answer (for context):
{formatted_answer}

Source extracts:
{corpus}
"""
    structred_llm=llm.with_structured_output(NewsSummary.model_json_schema())
    summary = structred_llm.invoke(prompt)
    history = state.get("history", []) or []
    history = history + [{"role": "assistant", "content": summary}]

    #return {"answer": summary}
    return {"answer": summary, "history": history}

    #return {"answer": summary}
    #return {"answer": summary, "history": history}



