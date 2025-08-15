from typing import List, Dict, Any
from backend.tools.executor import execute_actions

def run_executor(plan: List[Dict[str, Any]], analysis: str) -> List[Dict[str, Any]]:
    return execute_actions(plan, analysis)