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
    facts_str = "\n\n".join(facts) if facts else "No specific web facts available."
    
    # Requesting one paragraph, but TH has no manifold to ENFORCE it.
    prompt = f"Write ONE CONCISE PARAGRAPH summarizing {query} based on these summaries. ONE PARAGRAPH ONLY:\n\n{facts_str}"
    
    print(f"   > [TH] Generating (hopefully) concise strategic report...")
    response = llm.invoke(prompt)
    report = response.content if hasattr(response, 'content') else str(response)
    print(f"     [MSG PASS] Report generated: {report[:100]}...")
    
    return {"strategic_packet": report}
