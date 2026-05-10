from config.llm import get_llm
from state.schema import AgentState
from typing import Dict

llm = get_llm()

def strategic_agent(state: AgentState) -> Dict:
    """
    LAYER: STRATEGIC (TH - UNCONSTRAINED)
    """
    facts = state.get("tactical_packet", [])
    query = state.get("query", "Latest news")
    print(f"\n[TH] Entering Strategic Layer")
    print(f"   > [MSG IN] Received Tactical Packet:")
    for i, f in enumerate(facts):
        print(f"       [Fact Set {i+1}]: {f[:150].strip()}...")
    facts_str = "\n\n".join(facts) if facts else "No specific web facts available."
    
    # Identical base instruction for both TH and CTHA
    base_prompt = f"Synthesis of evidence into a singular stable statement. Summarize {query} based on provided facts. CONSTRAINTS: One concise paragraph. No markdown. Neutral tone."
    prompt = f"{base_prompt}\n\nEVIDENCE:\n{facts_str}"
    
    print(f"   > [TH] Generating (hopefully) concise strategic report...")
    response = llm.invoke(prompt)
    report = response.content if hasattr(response, 'content') else str(response)
    print(f"     [MSG PASS] Report generated.")
    
    print(f"   > [MSG OUT] Passing Strategic Packet to Institutional:\n       {report.strip()}")
    return {"strategic_packet": report}
