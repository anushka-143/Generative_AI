from langchain.agents import initialize_agent,Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
wikipedia_tool = Tool(
    name = "Wikipedia Search",
    func=WikipediaAPIWrapper().run,
    description="Use this tool to search Wikipedia for information on any topic"
)
searchtool = Tool(
    name = "DuckDuckGo Search",
    func = DuckDuckGoSearchRun().run,
    description="use this tool to perform web searches using DuckDuckGo"
)
llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-pro",
    temperature = 0.5,
    max_tokens = None,
    timeout = None,
    max_retries = 2,
)
tools = [wikipedia_tool,searchtool]
agent = initialize_agent(tools=tools,llm = llm, agent="zero-shot-react-description",verbose=True)

query = "Tell me about the History of Agentic AI."
response = agent.run(query)
print("Response from Agent: ", response)

