from langchain_core.agents import AgentAction,AgentFinish
from langgraph.graph import END,StateGraph
from nodes import reason_node,act_node
from state import AgentState
from dotenv import load_dotenv

load_dotenv()

graph=StateGraph(AgentState)

REASON_NODE="reason_node"
ACT_NODE="act_node"

def should_continue(state:AgentState)->str:
    if isinstance(state["agent_outcome"],AgentFinish):
        return END
    else:
        return ACT_NODE

graph.add_node(REASON_NODE,reason_node)
graph.add_node(ACT_NODE,act_node)
graph.set_entry_point(REASON_NODE)
graph.add_conditional_edges(REASON_NODE,should_continue)
graph.add_edge(ACT_NODE,REASON_NODE)
app=graph.compile()

res=app.invoke(
    {
    "input":"How many days ago was the latest SpaceX launch?",
    "agent_outcome":None,
    "intermediate_steps":[]
    }
)

print(res)

print(res["agent_outcome"].return_values["output"],"final_result")