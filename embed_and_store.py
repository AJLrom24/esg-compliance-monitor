from document_ingestor import ingest_documents

SOURCE_DIR = "resources/"
PERSIST_DIR = "vectorstore/"

ingest_documents(SOURCE_DIR, PERSIST_DIR)

