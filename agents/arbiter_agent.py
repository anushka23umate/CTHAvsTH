from typing import Dict
from ctha.contracts import validate_contract
from state.schema import AgentState

def arbiter_agent(state: AgentState) -> Dict:
    """
    The CTHA Arbiter Agent.
    Implements the 'Arbiter Resolution Constraint' (CR3).
    """
    print("\n--- [ARBITER] Applying Resolution Constraints ---")
    
    is_valid = validate_contract(state)
    current_retries = state.get("retry_count", 0)
    
    if is_valid:
        print("   > [ARBITER] Stability Confirmed. State sits on the Valid Manifold.")
        return {
            "arbiter_signal": "PROCEED",
            "is_contract_valid": True
        }
    else:
        print("   > [ARBITER] COORDINATION STABILITY FAILURE DETECTED!")
        print(f"   > [ARBITER] Reason: Inter-layer message conflict or noisy evidence (Attempt {current_retries + 1}).")
        
        # Increment temporal count (backtrack)
        return {
            "arbiter_signal": "BACKTRACK",
            "is_contract_valid": False,
            "retry_count": current_retries + 1
        }
