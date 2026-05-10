from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    query: str
    reflex_packet: List[Dict]
    tactical_packet: List[str]
    tactical_packet_projected: Dict[str, Any]
    strategic_packet: str
    institutional_packet: str
    final_answer: str
    arbiter_signal: str  # CRITICAL: Controls the CTHA flow
    retry_count: int
    authority_scope: str
    is_contract_valid: bool
    
    # Efficient Infrastructure Design variables
    step_count: int
    goal_completed: bool
    session_boundary: bool
    cached_messages: Dict[str, Any]