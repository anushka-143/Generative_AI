# 📚 Educational AI Agent - README.md

An intelligent research assistant built with **LangChain**, **Streamlit**, and **Gemini** to help users explore and learn about any topic through reliable sources like **Wikipedia** and **Arxiv**.

🟢 **[Try it Live](https://educational-researchapp.streamlit.app/)**

---

## 🚀 Features

- 🤖 Powered by Google's Gemini (`gemini-2.5-flash`)
- 📚 Tool support: Wikipedia and Arxiv (LangChain tools)
- 🧠 Zero-shot agent reasoning using `initialize_agent`
- 🧾 Verbose output showing the agent's step-by-step reasoning
- 🎯 Clean, responsive UI using Streamlit

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
