import operator
from typing import Annotated,List,Union,TypedDict
from langchain_core.agents import AgentAction,AgentFinish

class AgentState(TypedDict):
    input:str
    agent_outcome:Union[AgentFinish,AgentAction,None]
    intermediate_steps:Annotated[List[tuple[AgentAction,str]],operator.add]