import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser



load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-pro",
    temperature = 0,
    max_tokens = None,
    timeout = None,
    max_retries = 2,
)

prompt = ChatPromptTemplate([
    ("system", "You are a helpful assistant, that translates language from {input_language} to {output_language}"),
    ("human", "{input}")

])

st.title("translator using Gemini")
input_text = st.text_input("Enter your sentence in English and it will be translated to Japanese")

output_parser = StrOutputParser()

chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({
        "input_language": "English",
        "output_language": "Japanese",
        "input": input_text
    }))