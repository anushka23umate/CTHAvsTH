from state.schema import AgentState
from config.llm import get_llm
from ctha.contracts import PMsum, PMplan
from agents.reflex_agent import reflex_agent as raw_reflex
from typing import Dict

llm = get_llm()

def ctha_reflex_agent(state: AgentState) -> Dict:
    retry_count = state.get("retry_count", 0)
    query = state.get("query", "")
    
    if retry_count > 0:
        refined_query = f"{query} verified reports"
        print(f"\n--- [CTHA] Conflict Resolution: Refining query to: {refined_query} ---")
    else:
        refined_query = query
    
    print(f"\n--- [CTHA] Entering Reflex Manifold (Attempt {retry_count + 1}) ---")
    res = raw_reflex({**state, "query": refined_query})
    
    raw_packet = res.get("reflex_packet", [])
    filtered_packet = PMsum(raw_packet)
    
    print(f"   > [FLOW] Reflex -> Tactical: Passing {len(filtered_packet)} projected sources.")
    return {
        "reflex_packet": filtered_packet,
        "query": refined_query
    }

def ctha_tactical_agent(state: AgentState) -> Dict:
    data = state.get("reflex_packet", [])
    print("\n--- [CTHA] Entering Tactical Manifold ---")
    print(f"   > [FLOW] Tactical received {len(data)} raw data packets.")
    
    summaries = []
    if data:
        for i, d in enumerate(data):
            prompt = f"Extract 5 technical facts from this news source.\nCONTENT: {d['content'][:3000]}"
            print(f"   > [CTHA] Distilling Structured Fact Set {i+1}")
            response = llm.invoke(prompt)
            summary = response.content if hasattr(response, 'content') else str(response)
            summaries.append(summary)
            print(f"     [MSG PASS] Source {i+1} distilled: {summary[:100]}...")

    projected = PMplan(summaries)
    return {
        "tactical_packet": summaries,
        "tactical_packet_projected": projected
    }

def ctha_strategic_agent(state: AgentState) -> Dict:
    print("\n--- [CTHA] Entering Strategic Manifold ---")
    plan = state.get("tactical_packet_projected", {})
    query = state.get("query", "")
    
    if not plan.get("is_stable", False):
        print("   > [CTHA] POLICY ENFORCEMENT: Stability Violation detected.")
        return {"strategic_packet": f"STABILITY_FAILURE: Evidence manifold for '{query}' is insufficient."}
    
    facts_str = "\n\n".join(plan.get("payload", []))
    print(f"   > [FLOW] Strategic received {len(plan.get('payload', []))} stable facts.")
    
    prompt = f"Write a research report on {query} using these {plan.get('fact_count')} verified sources:\n{facts_str}"
    
    print(f"   > [CTHA] Drafting Strategic Report...")
    response = llm.invoke(prompt)
    draft = response.content if hasattr(response, 'content') else str(response)
    print(f"     [MSG PASS] Draft generated: {draft[:100]}...")
    return {"strategic_packet": draft}

def ctha_institutional_agent(state: AgentState) -> Dict:
    print("\n--- [CTHA] Entering Institutional Manifold ---")
    draft = state.get("strategic_packet", "")
    query = state.get("query", "")
    
    if "STABILITY_FAILURE" in draft:
        return {"final_answer": f"ERROR: CTHA Stability Failure. No grounded evidence found for query: {query}"}

    print(f"   > [FLOW] Institutional reviewing draft ({len(draft)} chars).")
    prompt = f"Format this research report professionally.\nCONTENT: {draft}"
    response = llm.invoke(prompt)
    from ctha.contracts import PMpol
    final = response.content if hasattr(response, 'content') else str(response)
    return {"final_answer": PMpol(final)}
