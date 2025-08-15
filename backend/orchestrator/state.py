from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

# You can persist this in a DB if needed.
class MemoryItem(BaseModel):
    role: Literal["user", "system", "assistant", "tool"]
    content: str

class OrchestratorState(BaseModel):
    # Full conversation context
    messages: List[MemoryItem] = Field(default_factory=list)

    # Planner output
    plan: Optional[List[Dict[str, Any]]] = None  # JSON steps

    # Research output
    context_chunks: Optional[List[str]] = None

    # Analysis output
    analysis: Optional[str] = None
    violations: Optional[List[str]] = None

    # Executor output
    actions_taken: Optional[List[Dict[str, Any]]] = None

    # Control flags
    done: bool = False