from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

from backend.orchestrator.state import OrchestratorState, MemoryItem
from backend.agents.planner import plan_steps
from backend.agents.research import run_research
from backend.agents.analysis import analyze
from backend.agents.executor import run_executor
from backend.orchestrator.data_creator import add_pdf_to_chroma

# ---------- Node definitions ----------

def node_planner(state: OrchestratorState) -> OrchestratorState:
    llm = ChatOllama(model="tinyllama", temperature=0.2)
    user_msg = next((m.content for m in reversed(state.messages) if m.role == "user"), "")
    state.plan = plan_steps(llm, user_msg)
    return state

def node_research(state: OrchestratorState) -> OrchestratorState:
    user_msg = next((m.content for m in reversed(state.messages) if m.role == "user"), "")
    # Allow plan to override k
    k = 5
    for step in (state.plan or []):
        if step.get("agent") == "research":
            k = step.get("params", {}).get("k", 5)
            break
    state.context_chunks = run_research(user_msg, k=k)
    return state

def node_analysis_node(state: OrchestratorState) -> OrchestratorState:
    llm = ChatOllama(model="tinyllama", temperature=0.2)
    user_msg = next((m.content for m in reversed(state.messages) if m.role == "user"), "")
    analysis_result, violations = analyze(llm, user_msg, state.context_chunks or [])
    state.analysis = analysis_result
    state.violations = violations
    return state

def node_executor(state: OrchestratorState) -> OrchestratorState:
    # If there are violations, block execution
    if state.violations:
        state.actions_taken = [{"status": "blocked", "reason": f"Policy violations: {', '.join(state.violations)}"}]
        state.done = True
        return state

    plan_steps_only = [s for s in (state.plan or []) if s.get("agent") == "executor"]
    state.actions_taken = run_executor(plan_steps_only, state.analysis or "")
    state.done = True
    return state

# ---------- Router / Conditional edges ----------

def should_research(state: OrchestratorState) -> bool:
    return any(s.get("agent") == "research" for s in (state.plan or []))

def should_analyze(state: OrchestratorState) -> bool:
    return any(s.get("agent") == "analysis" for s in (state.plan or []))

def should_execute(state: OrchestratorState) -> bool:
    return any(s.get("agent") == "executor" for s in (state.plan or []))

# ---------- Build the graph ----------

def build_graph():
    g = StateGraph(OrchestratorState)

    g.add_node("planner", node_planner)
    g.add_node("research", node_research)
    g.add_node("analysis_node", node_analysis_node)  # renamed node
    g.add_node("executor", node_executor)

    # Start with planner
    g.set_entry_point("planner")

    # Conditional edges based on plan content
    g.add_conditional_edges(
        "planner",
        lambda s: "research" if should_research(s) else ("analysis_node" if should_analyze(s) else ("executor" if should_execute(s) else END)),
        {"research": "research", "analysis_node": "analysis_node", "executor": "executor", END: END}
    )

    # After research -> analysis or executor
    g.add_conditional_edges(
        "research",
        lambda s: "analysis_node" if should_analyze(s) else ("executor" if should_execute(s) else END),
        {"analysis_node": "analysis_node", "executor": "executor", END: END}
    )

    # After analysis -> executor or END
    g.add_conditional_edges(
        "analysis_node",
        lambda s: "executor" if should_execute(s) else END,
        {"executor": "executor", END: END}
    )

    # End
    g.add_edge("executor", END)

    return g.compile()

# Singleton app graph
app_graph = build_graph()

def run_orchestrator(user_text: str) -> Dict[str, Any]:
    add_pdf_to_chroma("leave_policy.pdf")
    # Initialize state with user message
    state = OrchestratorState(messages=[MemoryItem(role="user", content=user_text)])
    final_state: OrchestratorState = app_graph.invoke(state)
    return dict(final_state)