from state import AgentState
from runnable import tools,react_runnable
from dotenv import load_dotenv

load_dotenv()
def reason_node(state:AgentState):
    agent_outcome=react_runnable.invoke(state)
    return {"agent_outcome":agent_outcome}

def act_node(state:AgentState):
    agent_action=state["agent_outcome"]
    tool_name=agent_action.tool
    tool_input=agent_action.tool_input
    tool_function=None

    for i in tools:
        if i.name==tool_name:
            tool_function=i
            break
    if tool_function:
        if isinstance(tool_input,dict):
            op=tool_function.invoke(**tool_input)
        else:
            op=tool_function.invoke(tool_input)
    else:
        op=f"Tool '{tool_name} not found"
    return {"intermediate_steps":[(agent_action,str(op))]}