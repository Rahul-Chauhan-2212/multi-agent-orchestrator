from typing import List, Tuple
from langchain_ollama import ChatOllama
from backend.tools.rules import evaluate_policies

SYSTEM = (
    "You are an analysis agent. Given user question and retrieved context, "
    "produce a concise answer that cites snippets. Keep it factual and short."
)

def analyze(llm: ChatOllama, user_message: str, context_chunks: List[str]) -> Tuple[str, List[str]]:
    context_text = "\n\n---\n".join(context_chunks[:8])
    prompt = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Question: {user_message}\n\nContext:\n{context_text}"},
    ]
    result = llm.invoke(prompt).content
    violations, ok = evaluate_policies(result)
    return result, violations