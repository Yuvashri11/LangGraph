from langchain.agents import tool,create_react_agent,Tool
import datetime
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain import hub
import os
from langchain_groq import ChatGroq


load_dotenv()
groq_api_key=os.environ['GROQ_API_KEY']

llm=ChatGroq(model_name="Gemma2-9b-It",groq_api_key=groq_api_key)

@tool
def get_current_datetime(format:str="%Y-%m-%d %H:%M:%S"):
    """Returns the current date and time in YYYY-MM-DD HH:MM:SS format."""
    curr=datetime.datetime.now()
    return curr.strftime(format)


search_tools=TavilySearchResults(api_key=os.environ['TAVILY_API_KEY'],search_depth="basic")
tools=[search_tools, get_current_datetime]

prompt=hub.pull("hwchase17/react")

react_runnable=create_react_agent(tools=tools,llm=llm,prompt=prompt)