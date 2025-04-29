from asyncio import timeout
from http.client import responses
from tabnanny import verbose

from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import langchain
load_dotenv()

from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun

searchtool = Tool(
    name = "DuckDuckGo Search",
    func = DuckDuckGoSearchRun().run,
    description="use this tool to perform web searches using DuckDuckGo"
)
llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-pro",
    temperature = 0,
    max_tokens=None,
    timeout = None,
    max_retries = 2,
)
tools = [
    Tool(
        name = "Search",
        func=searchtool.run,
        description="Use this tool to perform web searches."
    )]
agent = initialize_agent(tools,llm, agent="zero-shot-react-description", verbose = True)
response = agent.run("What are the current affairs in India of this week?")
print(response)