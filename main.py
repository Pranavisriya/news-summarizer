from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from pydantic import BaseModel, Field # type: ignore
from create_workflow import create_agent
from typing import Optional, List, Any
from typing import Optional
import os

# # app = FastAPI(
# #     title="News Summarizer API",
# #     description="LangGraph-based news summarizer",
# #     version="1.0.0",
# # )

# # class AskRequest(BaseModel):
# #     question: str = Field(..., description="User query to summarize, e.g., 'delhi red fort blast'")
# #     thread_id: Optional[str] = Field("1", description="Optional thread id if you want to isolate memory")

# # class Reply(BaseModel):
# #     summary: str
# #     sources: List[str] = []

# # class AnswerOut(BaseModel):
# #     reply: Reply
# # class AskResponse(BaseModel):
# #     reply: Reply
# #     #answer: str


# # @app.get("/")
# # def greet():
# #     return {"message": "Welcome to the News Summarizer API!"}
# # @app.get("/")
# # def health():
# #     return {"ok": True} 

# # @app.post("/answer", response_model=AskResponse)
# # def post_answer(payload: AskRequest):
# #     resp = create_agent(payload.question, payload.thread_id)
# #     return AskResponse(answer=resp)

# # # @app.post("/ask", response_model=AskResponse, tags=["summarizer"])
# # # def ask(req: AskRequest):
# # #     try:
# # #         # Your create_agent already handles LangGraph execution and returns a string
# # #         answer = create_agent(req.question)
# # #         return AskResponse(answer=answer)
# # #     except Exception as e:
# # #         # Surface a clean error to the client
# # #         raise HTTPException(status_code=500, detail=str(e))
# # main.py






# # main.py
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Optional, Any
# import json

# from create_workflow import create_agent  # your function

# app = FastAPI(title="Assignment API")

# class AnswerIn(BaseModel):
#     thread_id: Optional[str] = "1"
#     user_text: str

# class AnswerOut(BaseModel):
#     # This will be a STRING that contains JSON text
#     answer: str

# def answer(thread_id: Optional[str], user_text: str) -> Any:
#     return create_agent(user_text)

# @app.post("/answer", response_model=AnswerOut)
# def post_answer(payload: AnswerIn):
#     try:
#         resp = answer(payload.thread_id, payload.user_text)

#         # Convert to JSON string no matter what
#         if isinstance(resp, (dict, list)):
#             json_str = json.dumps(resp, ensure_ascii=False)
#         elif isinstance(resp, str):
#             # If it's already JSON, keep as-is; otherwise wrap
#             try:
#                 json.loads(resp)  # validate
#                 json_str = resp
#             except Exception:
#                 json_str = json.dumps({"summary": resp}, ensure_ascii=False)
#         else:
#             # Fallback: stringify then wrap
#             json_str = json.dumps({"summary": str(resp)}, ensure_ascii=False)

#         return {"answer": json_str}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import Optional, Any
import json
 # make sure this matches your filename

app = FastAPI(title="Assignment API")

class AnswerIn(BaseModel):
    thread_id: Optional[str] = "1"
    user_text: str

class AnswerOut(BaseModel):
    answer: str  # JSON string

def answer_fn(thread_id: Optional[str], user_text: str) -> Any:
    # ✅ pass thread_id through to create_agent
    return create_agent(user_query=user_text, thread_id=thread_id or "1")

@app.post("/answer", response_model=AnswerOut)
def post_answer(payload: AnswerIn):
    try:
        resp = answer_fn(payload.thread_id, payload.user_text)

        # Normalize to JSON string
        if isinstance(resp, (dict, list)):
            json_str = json.dumps(resp, ensure_ascii=False)
        elif isinstance(resp, str):
            try:
                json.loads(resp)  # already JSON
                json_str = resp
            except Exception:
                json_str = json.dumps({"summary": resp}, ensure_ascii=False)
        else:
            json_str = json.dumps({"summary": str(resp)}, ensure_ascii=False)

        return {"answer": json_str}
    except Exception as e:
        # If you still hit 500, it's almost always due to missing env vars or a bad import
        raise HTTPException(status_code=500, detail=str(e))
