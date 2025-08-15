import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader

# Config
CHROMA_DIR = os.getenv("CHROMA_DIR", "data/chroma")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
COLLECTION_NAME = "docs"  # Must match your retriever

def add_pdf_to_chroma(pdf_path: str):
    """
    Add a PDF's content to the Chroma vector store if not already present.
    """
    pdf_name = os.path.basename(pdf_path).lower()
    # Connect to existing Chroma
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    # Fetch all existing docs metadata
    all_docs = vectorstore.get(include=["metadatas"])
    for meta in all_docs["metadatas"]:
        if meta and "source" in meta and os.path.basename(meta["source"]).lower() == pdf_name:
            print(f"⚠️ PDF '{pdf_name}' already exists in Chroma. Skipping.")
            return False

    # Load new PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Store filename in metadata
    for doc in documents:
        doc.metadata["source"] = pdf_path

    vectorstore.add_documents(documents)
    vectorstore.persist()

    print(f"✅ PDF '{pdf_name}' added to Chroma.")
    return True