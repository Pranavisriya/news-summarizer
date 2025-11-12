from state import AgentState, NewsSummary
from langchain_openai import ChatOpenAI # type: ignore
from langchain_core.messages import SystemMessage, HumanMessage # type: ignore
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

OPEN_API_KEY= os.getenv("OPEN_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",     
    temperature=0.0,
    api_key=OPEN_API_KEY
)

# 
def rewrite_query(state: AgentState):
    user_question = (state.get("question") or "").strip()
    history = state.get("history", []) or []

    context = "\n".join(f"{m.get('role','user')}: {m.get('content','')}" for m in history[-6:])

    system_prompt = (
        "You rewrite a user's message into ONE precise web-search query.\n"
        "Rules:\n"
        "- Stay strictly on the same incident/topic suggested by the provided context/history.\n"
        "- Include WHERE and WHEN if present.\n"
        "- Use 3–8 essential keywords; remove filler.\n"
        "- If the prompt is vague (e.g., 'government reaction on this'), assume SAME incident.\n"
        "- Output ONLY the final query string (no quotes)."
    )
    user_prompt = f"""[CONTEXT]
{context}

[USER MESSAGE]
{user_question}

[INSTRUCTION]
Rewrite into ONE precise on-topic web search query for the SAME incident/date/location.
Only the query string."""
    msg = llm.invoke([SystemMessage(content=system_prompt),
                      HumanMessage(content=user_prompt)])
    rewritten = (getattr(msg, "content", "") or "").strip()
    if len(rewritten) > 1 and rewritten[0] in ("'", '"', "`") and rewritten[-1] == rewritten[0]:
        rewritten = rewritten[1:-1].strip()
    return {"question": rewritten or user_question}
