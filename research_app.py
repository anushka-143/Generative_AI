import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
import os

# Load environment variables (ensure GOOGLE_API_KEY and serpAPI is set in your .env file)
# In a Streamlit deployment, you would set this as a secret.
# For local testing, create a .env file in the same directory as your script:
from dotenv import load_dotenv

load_dotenv()

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Educational AI Agent", layout="wide")
st.title("📚 Educational AI Agent")
st.markdown("""
This agent leverages multiple tools (Wikipedia, DuckDuckGo, Arxiv) to provide comprehensive answers to your queries.
It's designed to help you explore and learn about various topics.
""")


# --- LangChain Agent Initialization (Cached for performance) ---
@st.cache_resource
def initialize_langchain_agent():
    """Initializes and caches the LangChain agent."""
    # Step 1: Define all the tools
    wikipedia_tool = Tool(
        name="Wikipedia Search",
        func=WikipediaAPIWrapper().run,
        description="Use this tool to search Wikipedia for information on any topic."
    )

    arxiv_tool = Tool(
        name="Arxiv Search",
        func=ArxivQueryRun().run,
        description="Use this tool to search academic papers on arXiv. Provide topics, authors, or keywords for research-oriented queries."
    )

    search_tool = Tool(
        name= "SerpAPI tool",
        func= SerpAPIWrapper().run,
        description= "Use this tool to search on web for updated or recent data/information"
    )

    research_tool = Tool(
        name = "SemanticScholar tool",
        func= SemanticScholarQueryRun().run,
        description= "Use this tool for scientific literature or for more academic context"
    )


    # Step 2: Initialize the LLM
    # Ensure GOOGLE_API_KEY is available as an environment variable
    if "GOOGLE_API_KEY" not in os.environ:
        st.error(
            "`GOOGLE_API_KEY` environment variable not found. Please set it in your `.env` file or Streamlit secrets.")
        st.stop()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Step 3: Combine all the tools into a list
    tools = [wikipedia_tool, arxiv_tool, search_tool, research_tool]

    # Step 4: Initialize the Agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True# Keep verbose for educational insights
    )
    return agent


# Initialize the agent
agent = initialize_langchain_agent()

# --- User Input ---
query = st.text_area("Enter your query:")

# --- Agent Execution ---
if st.button("Get Answer"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Thinking... This might take a moment as the agent uses its tools..."):
            try:
                # Capture the agent's verbose output
                # We'll redirect stdout to capture the verbose output
                import io
                from contextlib import redirect_stdout

                f = io.StringIO()
                with redirect_stdout(f):
                    response = agent.run(query)

                verbose_output = f.getvalue()

                st.subheader("Response from Agent:")
                st.write(response)

                st.subheader("Agent's Thought Process (Verbose Output):")
                st.code(verbose_output, language='text')

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info(
                    "Please ensure your `GOOGLE_API_KEY` is correctly set and you have an active internet connection.")

st.markdown("---")
