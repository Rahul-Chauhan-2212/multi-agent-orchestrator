from typing import List
from .utils import clamp_len
from backend.tools.retriever import simple_rag_query

def run_research(query: str, k: int = 5) -> List[str]:
    chunks = simple_rag_query(query=query, k=k)
    return [clamp_len(c, 2000) for c in chunks]