from config.llm import get_llm
from state.schema import AgentState

llm = get_llm()

def strategic_agent(state: AgentState) -> AgentState:
    """
    LAYER: STRATEGIC (TH - UNCONSTRAINED)
    Responsibility: Writing a report.
    Communication: Free Natural Language.
    """
    facts = state.get("tactical_packet", [])
    query = state.get("query", "")
    facts_str = "\n\n".join(facts) if facts else "No specific web facts available."
    
    print(f"   > [TH] Generating unconstrained strategic report...")
    
    # TH: Naive prompt that accepts raw, unvalidated natural language from below.
    prompt = f"""
    Write a long, detailed research report about: {query}
    
    Use all of this information:
    {facts_str}
    
    Make it as long and comprehensive as possible.
    """
    
    response = llm.invoke(prompt)
    draft = response.content if hasattr(response, 'content') else str(response)
    
    return {**state, "strategic_packet": draft}
