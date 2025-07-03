# 📚 Educational AI Agent - README.md

This is a **multi-tool AI assistant** built with **LangChain** and **Streamlit**, designed to provide comprehensive answers to user queries by leveraging:
- Wikipedia
- Arxiv academic papers
- DuckDuckGo (optionally, can be extended)
- Google's Gemini (via `ChatGoogleGenerativeAI`)

---

## 🚀 Features

- 🤖 Uses Google Gemini (`gemini-2.5-flash`) for natural language understanding
- 🔍 Integrates Wikipedia and Arxiv tools for search
- 🧠 Zero-shot agent with reasoning capabilities
- 🧾 Shows agent's thought process (verbose reasoning)
- 🧱 Built with `LangChain`, `Streamlit`, and `dotenv`

---

## 🛠️ Setup Instructions

```bash
git clone https://github.com/anushka-143/Generative_AI.git
cd Generative_AI

## 🛠️ Setup Instructions

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt

Create a .env file in the root directory and add your Google API key:
GOOGLE_API_KEY=your_google_api_key_here

▶️ Run the App

streamlit run app.py

## 🧠 How It Works

### 🔹 LLM Setup
Loads the Gemini model (`gemini-2.5-flash`) via `ChatGoogleGenerativeAI`.

### 🔹 Tool Initialization
Adds Wikipedia and Arxiv search tools using LangChain's standard wrappers.

### 🔹 Agent Creation
Uses LangChain's `initialize_agent` with `zero-shot-react-description` and verbose mode for detailed reasoning.

### 🔹 Query Execution
- User submits a query  
- The agent selects relevant tools and processes the input  
- Displays both the final answer and its reasoning trace

---

## 📦 Dependencies

- `streamlit`  
- `langchain`  
- `langchain-google-genai`  
- `langchain_community`  
- `python-dotenv`

---

## 📌 Notes

- Ensure a stable internet connection while using the app.  
- The `GOOGLE_API_KEY` must be active and have access to Gemini.  
- This app is built for educational and experimental use.
