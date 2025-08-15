from typing import Dict, Any, List

# Real integrations would call Slack/Jira/Email. We just simulate.
def execute_actions(plan_steps: List[Dict[str, Any]], analysis: str) -> List[Dict[str, Any]]:
    results = []
    for step in plan_steps:
        action = step.get("action")
        params = step.get("params", {})
        results.append({"action": action, "params": params, "status": "ok", "note": f"Simulated with analysis: {analysis[:60]}..."})
    return results