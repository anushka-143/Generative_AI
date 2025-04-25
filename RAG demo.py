from langchain_community.document_loaders import UnstructuredURLLoader
urls = ["https://victoriaonmove.com.au/local-removalists.html", "https://victoriaonmove.com.au/index.html", "https://victoriaonmove.com.au/contact.html"]
loader = UnstructuredURLLoader(urls=urls)
data = loader.load()

#print(data)

from langchain.text_splitter import RecursiveCharacterTextSplitter

#split data into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(data)
print("Number of documents:", len(docs))


from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


vectorstore = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type = "similarity", search_kwargs= {"k":6})
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-pro",
    temperature = 0.4,
    max_tokens=500,
    timeout = None,
    max_retries = 2,
)

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

system_prompt= (
    "You are an assistant for question-answering tasks."
    "Use the following pieces of retrieved context to answer"
    "the question. if you dont know the answer, say thank you"
    "don't know. use three sentences maximum and keep the answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human","{input}"),
    ]
)
que_ans_chain = create_stuff_documents_chain(llm,prompt)
rag_chain = create_retrieval_chain(retriever,que_ans_chain)

response = rag_chain.invoke({"input":"What kind of services they provide?"})
print(response["answer"])
