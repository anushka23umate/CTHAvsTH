from config.llm import get_llm
from state.schema import AgentState

llm = get_llm()

def tactical_agent(state: AgentState) -> AgentState:
    """
    LAYER: TACTICAL (TH - UNCONSTRAINED)
    Responsibility: Loose information summary.
    Communication: Free Natural Language.
    """
    data = state.get("reflex_packet", [])
    
    if not data:
        return {**state, "tactical_packet": [], "is_contract_valid": False}

    print(f"   > [TH] Distilling info via unconstrained summary...")
    summaries = []
    for d in data:
        # TH: Unconstrained, loose prompt. Prone to hallucination if content is messy.
        prompt = f"Summarize this news source for me in detail. Include everything you think is important.\n\nCONTENT: {d['content'][:4000]}"
        
        response = llm.invoke(prompt)
        summary = response.content if hasattr(response, 'content') else str(response)
        summaries.append(summary)

    return {**state, "tactical_packet": summaries, "is_contract_valid": True}
