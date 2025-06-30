import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA

# --- Load API Key from Streamlit Secrets ---
openai_api_key = st.secrets["OPENAI_API_KEY"]

# --- Set up embeddings and vectorstore ---
PERSIST_DIR = "vectorstore/"
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
db = FAISS.load_local(PERSIST_DIR, embeddings, allow_dangerous_deserialization=True)

# --- Initialize retriever and LLM chain ---
retriever = db.as_retriever(search_kwargs={"k": 4})
llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# --- Streamlit UI ---
st.set_page_config(page_title="Sustainability / ESG InfoBot", page_icon="🌱")
st.title("🌱 Sustainability / ESG InfoBot")
st.write("Ask me about sustainability topics, ESG reports, or regulatory documents.")

query = st.text_input("Enter your question:")
if query:
    with st.spinner("Thinking..."):
        response = qa_chain.run(query)
        st.success(response)
