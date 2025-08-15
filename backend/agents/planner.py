from typing import List, Dict, Any
from langchain_ollama import ChatOllama

DEFAULT_SYSTEM = (
    "You are a planning agent. Break the user goal into a few high-level steps. "
    "Use JSON list of steps. Each step must have 'agent' in ['research','analysis','executor'] "
    "and an 'action' string and optional 'params'. Keep it minimal."
)

def plan_steps(llm: ChatOllama, user_message: str) -> List[Dict[str, Any]]:
    prompt = [
        {"role": "system", "content": DEFAULT_SYSTEM},
        {"role": "user", "content": user_message},
    ]
    resp = llm.invoke(prompt)
    # Try to parse JSON; fallback to a default heuristic.
    import json
    try:
        return json.loads(resp.content)
    except Exception:
        # Safe default 3-step plan
        return [
            {"agent": "research", "action": "retrieve_relevant_docs", "params": {"k": 5}},
            {"agent": "analysis", "action": "summarize_and_check_policies"},
            {"agent": "executor", "action": "propose_next_actions"},
        ]