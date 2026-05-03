from config.llm import get_llm
from state.schema import AgentState

llm = get_llm()

def institutional_agent(state: AgentState) -> AgentState:
    """
    LAYER: INSTITUTIONAL (TH - UNCONSTRAINED)
    Responsibility: Final formatting.
    Communication: Free Natural Language.
    """
    draft = state.get("strategic_packet", "")
    
    if not draft:
        return {**state, "final_answer": "ERROR: No content produced."}

    print(f"   > [TH] Applying loose final formatting...")
    
    # TH: Basic "make it look nice" prompt.
    prompt = f"Make this research report look professional and pretty. Keep the full text.\n\nREPORT:\n{draft}"
    
    try:
        response = llm.invoke(prompt)
        final = response.content if hasattr(response, 'content') else str(response)
        return {**state, "final_answer": final}
    except Exception as e:
        return {**state, "final_answer": draft}
