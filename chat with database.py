from sqlite3 import ProgrammingError

import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv
llm = GoogleGenerativeAI(
    model = "gemini-pro",
    google_api_key = os.environ["GOOGLE_API_KEY"]
)

from langchain.utilities import SQLDatabase
db_user = "root"
db_password = "root123"
db_host = "localhost"
db_name = "retail_sales_db"
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info =3)
print(db.table_info)


from langchain.chains import create_sql_query_chain
chain = create_sql_query_chain(llm, db)

def execute_query(question):
    try:
        #generate sql query from question
        response = chain.invoke({"question": "How many customers are there"})
        print(response)
        #Strip and format the query
        cleaned_query = response.strip("'''sql\n").strip("\n'''")
        print(cleaned_query)
        #execute the cleaned query
        result = db.run(cleaned_query)
        #display the result
        return cleaned_query, result
    except ProgrammingError as e:
        print(f"Ann error occurred: {e}")

st.title("Chat with SQL DB")
question = st.text_input("Enter your question:")
if st.button("Execute"):
    if question:
        cleaned_query, query_result = execute_query(question)
        if cleaned_query and query_result is not None:
            st.write("Generated SQL Query: ")
            st.code(cleaned_query, language="sql")
            st.write("Query result: ")
            st.write(query_result)
        else:
            st.write("No result returned due to an error")
    else:
        st.write("Please enter a question")
