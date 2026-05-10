from config.llm import get_llm
from state.schema import AgentState
from typing import Dict

llm = get_llm()

def tactical_agent(state: AgentState) -> Dict:
    """
    LAYER: TACTICAL (TH - UNCONSTRAINED)
    Forcing a smaller window to avoid 413 Payload error for the demo.
    """
    data = state.get("reflex_packet", [])
    print(f"\n[TH] Entering Tactical Layer")
    print(f"   > [MSG IN] Received Reflex Packet:")
    for i, d in enumerate(data):
        print(f"       - Source {i+1}: {d.get('url', 'Unknown')}")
    
    if not data:
        return {"tactical_packet": [], "is_contract_valid": False}

    # TRUNCATION: Only take top 2 sources to ensure we fit in the 8k context window
    demo_data = data[:2]
    print(f"   > [TH] Processing {len(demo_data)} sources (Truncated for Context Window).")
    
    summaries = []
    for i, d in enumerate(demo_data):
        base_prompt = "Extract 5 dense technical facts."
        prompt = f"{base_prompt}\n\nCONTENT: {d['content'][:1500]}"
        response = llm.invoke(prompt)
        summary = response.content if hasattr(response, 'content') else str(response)
        summaries.append(summary)
        print(f"     [MSG PASS] Source {i+1} summarized.")

    print(f"   > [MSG OUT] Passing Tactical Packet to Strategic:")
    for i, s in enumerate(summaries):
        print(f"       [Fact Set {i+1}]: {s[:150].strip()}...")
    return {"tactical_packet": summaries, "is_contract_valid": True}
