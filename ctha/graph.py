from langgraph.graph import StateGraph, END
from state.schema import AgentState
from ctha.agents import (
    ctha_reflex_agent, 
    ctha_tactical_agent, 
    ctha_strategic_agent, 
    ctha_institutional_agent
)
from agents.arbiter_agent import arbiter_agent

def arbiter_logic(state: AgentState):
    """
    CTHA 'Arbiter Resolution' routing.
    Strictly follows the signal emitted by the Arbiter node.
    """
    signal = state.get("arbiter_signal", "PROCEED")
    retries = state.get("retry_count", 0)
    
    if signal == "BACKTRACK" and retries < 3:
        print(f"   > [GRAPH] Stability failure detected. Backtracking to Reflex (Step {retries + 1}/3).")
        return "reflex"
    
    # If we hit the limit or have a PROCEED signal, move to Strategic
    if signal == "BACKTRACK":
        print("   > [GRAPH] Max retries reached. Stability cannot be guaranteed.")
    else:
        print("   > [GRAPH] Routing to Strategic layer.")
        
    return "strategic"

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("reflex", ctha_reflex_agent)
    graph.add_node("tactical", ctha_tactical_agent)
    graph.add_node("arbiter", arbiter_agent)
    graph.add_node("strategic", ctha_strategic_agent)
    graph.add_node("institutional", ctha_institutional_agent)

    graph.set_entry_point("reflex")

    graph.add_edge("reflex", "tactical")
    graph.add_edge("tactical", "arbiter")

    # The 'Bridge': Conditional edge based strictly on Arbiter output
    graph.add_conditional_edges("arbiter", arbiter_logic)

    graph.add_edge("strategic", "institutional")
    graph.add_edge("institutional", END)

    return graph.compile()