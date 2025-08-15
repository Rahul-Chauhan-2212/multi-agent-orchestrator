from typing import List, Tuple

# Extremely simple "rules engine" stub. Swap for OpenPolicyAgent, oso, or pyDatalog later.
POLICIES = [
    ("No PII in outbound messages", lambda text: any(tag in text.lower() for tag in ["ssn", "aadhaar", "passport"])),
    ("Do not email external recipients without approval", lambda text: "email" in text.lower() and "@gmail.com" in text.lower()),
]

def evaluate_policies(text: str) -> Tuple[List[str], bool]:
    violations = [name for name, predicate in POLICIES if predicate(text)]
    return violations, len(violations) == 0