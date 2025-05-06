from chains import generation_chain,reflection_chain
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from typing import List,Sequence
from langgraph.graph import END,MessageGraph

load_dotenv()

GENERATE="generate"
REFLECT="reflect"

graph=MessageGraph()

def gen_node(state):
    return generation_chain.invoke({"messages":state})

def ref_node(state):
    return reflection_chain.invoke({"messages":state})

graph.add_node(REFLECT,ref_node)
graph.add_node(GENERATE,gen_node)
graph.set_entry_point(GENERATE)

def should_continue(state):
    if (len(state)>4):
        return END
    return REFLECT

graph.add_conditional_edges(GENERATE,should_continue)
graph.add_edge(REFLECT,GENERATE)

app=graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

resp=app.invoke(HumanMessage(content="AI agents taking over content creation"))
print(resp)
