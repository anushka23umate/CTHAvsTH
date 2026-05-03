from config.llm import get_llm
from state.schema import AgentState
from typing import Dict

llm = get_llm()

def tactical_agent(state: AgentState) -> Dict:
    """
    LAYER: TACTICAL (TH - UNCONSTRAINED)
    Responsibility: Loose information summary.
    Communication: Free Natural Language.
    """
    data = state.get("reflex_packet", [])
    print(f"\n[TH] Entering Tactical Layer")
    print(f"   > [FLOW] Tactical received {len(data)} raw data packets.")
    
    if not data:
        return {"tactical_packet": [], "is_contract_valid": False}

    print(f"   > [TH] Distilling info via unconstrained summary...")
    summaries = []
    for i, d in enumerate(data):
        # TH: Unconstrained, loose prompt.
        prompt = f"Summarize this news source for me in detail. Include everything you think is important.\n\nCONTENT: {d['content'][:4000]}"
        
        response = llm.invoke(prompt)
        summary = response.content if hasattr(response, 'content') else str(response)
        summaries.append(summary)
        print(f"     [MSG PASS] Source {i+1} summarized: {summary[:100]}...")

    return {"tactical_packet": summaries, "is_contract_valid": True}
