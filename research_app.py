import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import io
from contextlib import redirect_stdout

# --- Load Env Vars ---
load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="📚 Educational AI Agent", layout="wide")
st.title("📚 Educational AI Agent")
st.markdown("An AI-powered assistant for learning, researching, and exploring academic topics using tools like Wikipedia, Arxiv, Semantic Scholar, and SerpAPI.")

# --- Session Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    def initialize_langchain_agent():
        wikipedia_tool = Tool(
            name="Wikipedia Search",
            func=WikipediaAPIWrapper().run,
            description="Use this tool to search Wikipedia for any topic."
        )
        arxiv_tool = Tool(
            name="Arxiv Search",
            func=ArxivQueryRun().run,
            description="Use this tool to search academic papers on arXiv."
        )
        serp_tool = Tool(
            name="Web Search",
            func=SerpAPIWrapper().run,
            description="Use this tool to search the internet for recent data using SerpAPI."
        )
        semscholar_tool = Tool(
            name="Semantic Scholar Search",
            func=SemanticScholarQueryRun().run,
            description="Use this tool for scientific literature and academic research."
        )

        if "GOOGLE_API_KEY" not in os.environ:
            st.error("`GOOGLE_API_KEY` is not set in .env or Streamlit secrets.")
            st.stop()

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.5,
            max_retries=2,
        )

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        agent = initialize_agent(
            tools=[wikipedia_tool, arxiv_tool, serp_tool, semscholar_tool],
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True,
            memory=memory,
            handle_parsing_errors=True,
        )
        return agent

    st.session_state.agent = initialize_langchain_agent()

# --- Display Previous Chat Messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input ---
if prompt := st.chat_input("Ask something about science, research, or any academic topic..."):
    # Show user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent typing...
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                f = io.StringIO()
                with redirect_stdout(f):
                    response = st.session_state.agent.run(prompt)
                verbose_output = f.getvalue()

                st.markdown(response)

                # Optionally show verbose agent reasoning:
                with st.expander("🔍 Agent Thought Process"):
                    st.code(verbose_output, language="text")

                # Save agent response
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                error_msg = f"❌ Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})


