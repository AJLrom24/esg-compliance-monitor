from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import tiktoken
import os

# Token-safe chunk splitter
def safe_split(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=lambda x: len(tiktoken.encoding_for_model("text-embedding-ada-002").encode(x))
    )
    return splitter.split_documents(documents)

def ingest_documents(source_dir, persist_dir):
    docs = []

    # Load PDF files page by page
    for file in os.listdir(source_dir):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(source_dir, file))
            docs.extend(loader.load_and_split())

    # Load .txt files
    for file in os.listdir(source_dir):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(source_dir, file))
            docs.extend(loader.load())

    print(f"📄 Loaded {len(docs)} documents.")

    # Split safely into chunks
    chunks = safe_split(docs)
    print(f"✂️ Split into {len(chunks)} chunks.")

    embeddings = OpenAIEmbeddings()
    batch_size = 50  # Safe number of chunks per embedding request

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    all_dbs = []
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_metadatas = metadatas[i:i + batch_size]
        sub_db = FAISS.from_texts(batch_texts, embeddings, metadatas=batch_metadatas)
        all_dbs.append(sub_db)

    # Merge all sub-indexes into one
    db = all_dbs[0]
    for sub_db in all_dbs[1:]:
        db.merge_from(sub_db)

    db.save_local(persist_dir)
    print(f"✅ Embeddings saved to: {persist_dir}")

