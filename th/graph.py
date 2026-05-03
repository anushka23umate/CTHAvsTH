from langgraph.graph import StateGraph, END
from state.schema import AgentState
from agents.reflex_agent import reflex_agent
from agents.tactical_agent import tactical_agent
from agents.strategic_agent import strategic_agent
from agents.institutional_agent import institutional_agent

def build_graph():
    """
    TH (Traditional Hierarchy)
    Unconstrained communication: layers follow each other linearly without validation.
    Errors propagate freely.
    """
    graph = StateGraph(AgentState)

    graph.add_node("reflex", reflex_agent)
    graph.add_node("tactical", tactical_agent)
    graph.add_node("strategic", strategic_agent)
    graph.add_node("institutional", institutional_agent)

    graph.set_entry_point("reflex")

    graph.add_edge("reflex", "tactical")
    graph.add_edge("tactical", "strategic")
    graph.add_edge("strategic", "institutional")
    graph.add_edge("institutional", END)

    return graph.compile()