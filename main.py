import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# App title
st.set_page_config(page_title="🌱 Sustainability / ESG InfoBot")
st.title("🌱 Sustainability / ESG InfoBot")
st.write("Ask me about Sustainability, ESG reports, or regulatory documents.")

# Load OpenAI API key from Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Initialize embeddings and LLM
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)

# Load vectorstore
PERSIST_DIR = "vectorstore/"
db = FAISS.load_local(PERSIST_DIR, embeddings, allow_dangerous_deserialization=True)

# Set up retrieval QA chain
retriever = db.as_retriever(search_kwargs={"k": 4})
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Query input
query = st.text_input("Enter your question:")
if query:
    with st.spinner("Thinking..."):
        try:
            response = qa_chain.run(query)
            st.success(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

