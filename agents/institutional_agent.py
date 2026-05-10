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
    
    print(f"\n[TH] Entering Institutional Layer")
    print(f"   > [MSG IN] Received Strategic Packet:\n       {draft.strip()}")

    if not draft:
        return {**state, "final_answer": "ERROR: No content produced."}

    print(f"   > [TH] Applying loose final formatting...")
    
    # TH: Unconstrained natural language attempt to enforce policy.
    prompt = f"Format this report as a single concise paragraph. DO NOT use any markdown formatting, headers, or bullet points.\n\nREPORT:\n{draft}"
    
    try:
        response = llm.invoke(prompt)
        final = response.content if hasattr(response, 'content') else str(response)
        print(f"   > [MSG OUT] Final Report ready for delivery:\n       {final.strip()}")
        return {**state, "final_answer": final}
    except Exception as e:
        return {**state, "final_answer": draft}
