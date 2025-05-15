from langgraph.graph import add_messages,StateGraph,END
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain_core.messages import AIMessage,HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver,sqlite3
import os

load_dotenv()

groq_api_key=os.environ['GROQ_API_KEY'] 

llm=ChatGroq(model_name="Gemma2-9b-It",groq_api_key=groq_api_key)

conn=sqlite3.connect("chat_db",check_same_thread=False)

mem=SqliteSaver(conn)

class basicState(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state:basicState):
    return {
        "messages":[llm.invoke(state["messages"])]
    }

graph=StateGraph(basicState)

graph.add_node("chatbot",chatbot)
graph.add_edge("chatbot",END)
graph.set_entry_point("chatbot")

app=graph.compile(checkpointer=mem)

config={"configurable":{
    "thread_id":1
}}
while True:
    
    user_input=input("User:")
    if user_input in ["exit","end"]:
        break
    result=app.invoke({
        "messages":[HumanMessage(content=user_input)]
    },config=config)
    print("AI:"+result["messages"][-1].content)