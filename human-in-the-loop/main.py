from langgraph.graph import add_messages,StateGraph,END
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain_core.messages import AIMessage,HumanMessage
from langchain_groq import ChatGroq
import os

load_dotenv()

groq_api_key=os.environ['GROQ_API_KEY']

llm=ChatGroq(model_name="Gemma2-9b-It",groq_api_key=groq_api_key)

class basicState(TypedDict):
    messages: Annotated[list,add_messages]


GENERATE="generate"
POST="post"
COLLECT_FEEDBACK="collect_feedback"
GET_REVIEW="get_review"

def generate(state:basicState):
    return {
        "messages":[llm.invoke(state["messages"])]
    }

def get_review(state:basicState):
    curr_content=state["messages"][-1].content
    print("Post content: \n"+curr_content)
    print("\n")

    decision=input("Can I post this content? (yes/no):")

    if decision.lower()=="yes":
        return POST
    else:
        return COLLECT_FEEDBACK
    
def collect_feedback(state:basicState):
    ip=input("How can I improve the post:")
    return {
        "messages":[HumanMessage(content=ip)]
    }

def post(state:basicState):
    resp=state["messages"][-1].content
    print("final post:\n")
    print(resp)
    print("\n")

graph=StateGraph(basicState)

graph.add_node(GENERATE,generate)
graph.add_node(POST,post)
graph.add_node(COLLECT_FEEDBACK,collect_feedback)
graph.add_node(GET_REVIEW,get_review)

graph.set_entry_point(GENERATE)
graph.add_conditional_edges(GENERATE,get_review)
graph.add_edge(POST,END)
graph.add_edge(COLLECT_FEEDBACK,GENERATE)

app=graph.compile()

app.invoke({
    "messages":[HumanMessage(content="AI agents taking over content creation")]
})