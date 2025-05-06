from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain.agents import tool,initialize_agent
import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-1.5-pro")


@tool
def get_current_datetime(format:str="%Y-%m-%d %H:%M:%S"):
    """Returns the current date and time in YYYY-MM-DD HH:MM:SS format."""
    curr=datetime.datetime.now()
    return curr.strftime(format)



search_tools=TavilySearchResults(search_depth="basic")
tools=[search_tools, get_current_datetime]
agent=initialize_agent(tools=tools,llm=llm,agent="zero-shot-react-description",verbose=True)
agent.invoke("give me a tweet about today's weather in Chennai")