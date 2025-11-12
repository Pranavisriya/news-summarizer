# from typing import TypedDict
# from typing import List
# from pydantic import BaseModel # type: ignore 
# import operator
# from typing import TypedDict, Annotated, List, Dict, Any

# class AgentState(TypedDict):
#     question: str
#     history: Annotated[List[Dict[str, str]], operator.add]
#     search_results: dict  
#     answer: str

# class NewsSummary(BaseModel):
#     summary: str
#     sources: List[str]
from typing import TypedDict, Annotated, List, Dict, Any
from pydantic import BaseModel
import operator

class AgentState(TypedDict, total=False):
    question: str
    history: Annotated[List[Dict[str, str]], operator.add]
    search_results: Dict[str, Any]
    answer: str

class NewsSummary(BaseModel):
    summary: str
    sources: List[str]
