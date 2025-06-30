import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment variables (make sure your .env has OPENAI_API_KEY)
load_dotenv()

# Initialize vector store
PERSIST_DIR = "vectorstore/"
embeddings = OpenAIEmbeddings()
db = FAISS.load_local(PERSIST_DIR, embeddings, allow_dangerous_deserialization=True)

# Set up retrieval-based QA chain
retriever = db.as_retriever(search_kwargs={"k": 4})
llm = ChatOpenAI(model="gpt-4")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Streamlit UI
st.title("🧠 ESG Compliance Assistant")
st.write("Ask me about sustainability, ESG reports, or regulatory documents.")

query = st.text_input("Enter your question:")
if query:
    with st.spinner("Thinking..."):
        response = qa_chain.run(query)
        st.success(response)


