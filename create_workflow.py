# from state import AgentState
# from search import search_web
# from generate_answer import generate_answer
# from summarize import summarize_answer
# from rewritequery import rewrite_query
# from langgraph.graph import StateGraph, END # type: ignore
# from langgraph.checkpoint.memory import InMemorySaver # type: ignore
# import os
# from langchain_core.runnables import RunnableConfig # type: ignore
# from dotenv import load_dotenv # type: ignore
# load_dotenv()

# OPEN_API_KEY= os.getenv("OPEN_API_KEY")

# def create_agent(user_query: str, thread_id: str) -> str:
#     """
#     Build the AI Agent Workflow

#     This creates a StateGraph where:
#     - Each node is an independent function that can read/update shared state
#     - LangGraph handles orchestration, state management, and execution flow
#     - Easy to extend: just add more nodes and define their connections
#     """
#     # Create the workflow graph
#     workflow = StateGraph(AgentState)

#     # Define our processing nodes
#     workflow.add_node("rewrite", rewrite_query)   # Step 0: Refine the query
#     workflow.add_node("search", search_web)        # Step 1: Gather information  
#     workflow.add_node("result", generate_answer)   # Step 2: Process and format
#     workflow.add_node("summarize", summarize_answer)  # Step 3: Final refinement

#     # Define the flow of intelligence
#     workflow.set_entry_point("rewrite")
#     workflow.add_edge("rewrite", "search")      # Start here
#     workflow.add_edge("search", "result") 
#     workflow.add_edge("result", "summarize")
#     workflow.add_edge("summarize", END)
#     #workflow.add_edge("result", END)        # After answer, we're done
#     checkpointer = InMemorySaver()

#     agent=workflow.compile(checkpointer=checkpointer)
#     config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
#     result=agent.invoke({"question": user_query}, config=config)
#     return result.get("answer", "")

# if __name__ == "__main__":
#     answer=create_agent("delhi red fort blast", "100")
#     print(answer)
#     answer=create_agent("government reaction on this incident", "100")
#     print(answer)
from state import AgentState
from search import search_web
from generate_answer import generate_answer
from summarize import summarize_answer
from rewritequery import rewrite_query
from langgraph.graph import StateGraph, END  # type: ignore
from langgraph.checkpoint.memory import InMemorySaver  # type: ignore
from langchain_core.runnables import RunnableConfig  # type: ignore

# ✅ create ONE saver and ONE compiled agent at import time
_checkpointer = InMemorySaver()

_workflow = StateGraph(AgentState)
_workflow.add_node("rewrite", rewrite_query)
_workflow.add_node("search", search_web)
_workflow.add_node("result", generate_answer)
_workflow.add_node("summarize", summarize_answer)

_workflow.set_entry_point("rewrite")
_workflow.add_edge("rewrite", "search")
_workflow.add_edge("search", "result")
_workflow.add_edge("result", "summarize")
_workflow.add_edge("summarize", END)

_agent = _workflow.compile(checkpointer=_checkpointer)

def create_agent(user_query: str, thread_id: str) -> str:
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
    result = _agent.invoke({"question": user_query}, config=config)
    return result.get("answer", "")
if __name__ == "__main__":
    answer = create_agent("delhi red fort blast", "100")
    print(answer)
    answer = create_agent("government reaction on this incident", "100")
    print(answer)