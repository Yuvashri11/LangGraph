from langgraph.graph import END,MessageGraph
from chains import first_responder_chain,revisor_chain
from tools import execute_tools
from langchain_core.messages import BaseMessage,ToolMessage
from typing import List

def responder(state)    :
    return first_responder_chain.invoke({"messages":state})

def revisor(messages):
    trimmed=messages[-5:]
    return revisor_chain.invoke({"messages":trimmed,"max_tokens": 500})
    
graph=MessageGraph()
graph.add_node("responder",responder)
graph.add_node("revisor",revisor)
graph.add_node("executor",execute_tools)

graph.add_edge("responder","executor")
graph.add_edge("executor","revisor")

max_itr=1
def should_continue(state:List[BaseMessage])->str:
    count_tool_visits=sum(isinstance(i,ToolMessage)for i in state)
    if count_tool_visits>max_itr:
        return END
    return "executor"

graph.add_conditional_edges("revisor",should_continue)
graph.set_entry_point("responder")

app=graph.compile()
print(app.get_graph().draw_mermaid())

response = app.invoke(
    "Write about how small business can leverage AI to grow for 50 words"
)

print(response[-1].tool_calls[0]["args"]["answer"])
print(response, "response")