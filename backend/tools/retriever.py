import os
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Configure via env vars
CHROMA_DIR = os.getenv("CHROMA_DIR", "data/chroma")

# Ollama embedding model name
# Common choices: "nomic-embed-text", "mxbai-embed-large"
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")


def get_retriever(collection_name: str = "docs", k: int = 5):
    """
    Create a retriever from a persisted Chroma vector store using Ollama embeddings.

    Args:
        collection_name (str): Name of the Chroma collection.
        k (int): Number of documents to retrieve.

    Returns:
        BaseRetriever: LangChain retriever object.
    """
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)
    vs = Chroma(
        collection_name=collection_name,
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    print(vs._collection.count())  # number of vectors stored
    return vs.as_retriever(search_kwargs={"k": k})


def simple_rag_query(query: str, k: int = 5) -> List[str]:
    """
    Run a simple RAG query on the persisted Chroma store.

    Args:
        query (str): User query string.
        k (int): Number of documents to retrieve.

    Returns:
        List[str]: List of retrieved document contents.
    """
    retriever = get_retriever(k=k)
    docs = retriever.get_relevant_documents(query)

    if not docs:
        print(f"No documents found for query: {query}")
        return []

    return [d.page_content for d in docs]