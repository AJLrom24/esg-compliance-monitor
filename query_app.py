import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document

# Load vectorstore
db = FAISS.load_local("vectorstore", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# Streamlit UI setup
st.set_page_config(page_title="ESG Assistant", layout="wide")
st.title("🧠 ESG Document Assistant")
st.write("Ask questions about your ESG documents — including CSRD, EFRAG, IFRS and more.")

query = st.text_input("🔍 Ask a question:", placeholder="e.g. What is the CSRD scope for non-EU companies?")

# Perform search on query
if query:
    with st.spinner("🔎 Searching your documents..."):
        docs: list[Document] = db.similarity_search(query, k=5)

    st.subheader("💬 Top Answers")

    for i, doc in enumerate(docs, 1):
        st.markdown(f"**{i}.** {doc.page_content.strip()}")
        meta = doc.metadata
        source = meta.get("source", "Unknown")
        page = meta.get("page", "N/A")
        st.caption(f"📄 Source: `{source}`  |  📄 Page: {page}")
        st.markdown("---")

