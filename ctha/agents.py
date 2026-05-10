from state.schema import AgentState
from config.llm import get_llm
from ctha.contracts import PMsum, PMplan, PMpol
from agents.reflex_agent import reflex_agent as raw_reflex
from typing import Dict

llm = get_llm()

def ctha_reflex_agent(state: AgentState) -> Dict:
    """
    ROLE: Reflex Layer - Fast execution and raw data aggregation.
    AUTHORITY SCOPE:
    - MAY: Perform web searches, scrape raw HTML.
    - MAY NOT: Interpret data, draw conclusions, or modify high-level goals.
    """
    retry_count = state.get("retry_count", 0)
    query = state.get("query", "")
    
    # Conflict Resolution logic (Arbiter-led backtracking)
    if retry_count > 0:
        refined_query = f"{query} verified research data and detailed reports"
        print(f"\n--- [CTHA] Arbiter Intervention: Backtracking with refined signal: {refined_query} ---")
    else:
        refined_query = query
    
    print(f"\n--- [CTHA] Reflex Manifold: Aggregating Execution State ---")
    res = raw_reflex({**state, "query": refined_query})
    raw_packet = res.get("reflex_packet", [])
    
    # PMsum Projection: Validate, Truncate, Sanitize
    filtered_packet = PMsum(raw_packet, max_sources=5)
    
    print(f"   > [FLOW] Reflex -> Tactical: Projecting {len(filtered_packet)} sources onto the Valid Manifold.")
    return {"reflex_packet": filtered_packet, "query": refined_query}

def ctha_tactical_agent(state: AgentState) -> Dict:
    """
    ROLE: Tactical Layer - Orchestrating information distillation and sequence management.
    AUTHORITY SCOPE:
    - MAY: Extract facts, maintain local working memory.
    - MAY NOT: Violate policy manifolds or ignore strategic plans.
    """
    data = state.get("reflex_packet", [])
    print("\n--- [CTHA] Tactical Manifold: Orchestrating Fact Extraction ---")
    print(f"   > [MSG IN] Received Reflex Packet:")
    for i, d in enumerate(data):
        print(f"       - Valid Source {i+1}: {d.get('url', 'Unknown')}")
    
    summaries = []
    if data:
        for i, d in enumerate(data):
            # Standardized Prompt Template with exact same base instruction
            base_prompt = "Extract 5 dense technical facts."
            prompt = (
                "ROLE: Fact Extractor\n"
                f"AUTHORITY: {base_prompt}\n"
                "COMMUNICATION: RECEIVE raw HTML. SEND fact set.\n"
                f"CONTENT: {d['content'][:3000]}"
            )
            print(f"   > [CTHA] Distilling Structured Fact Set {i+1}")
            response = llm.invoke(prompt)
            summary = response.content if hasattr(response, 'content') else str(response)
            summaries.append(summary)

    # PMplan Projection: Stability & Alignment Verification
    projected = PMplan(summaries, state.get("query", ""))
    print(f"   > [MSG OUT] Passing Projected Tactical Packet to Strategic:")
    for i, s in enumerate(projected.get('payload', [])):
        print(f"       [Stable Fact Set {i+1}]: {s[:150].strip()}...")
    return {"tactical_packet": summaries, "tactical_packet_projected": projected}

def ctha_strategic_agent(state: AgentState) -> Dict:
    """
    ROLE: Strategic Layer - High-level goal decomposition and stability monitoring.
    AUTHORITY SCOPE:
    - MAY: Request backtracks, reject unstable evidence.
    - MAY NOT: Perform low-level execution.
    """
    print("\n--- [CTHA] Strategic Manifold: Goal Decomposition & Stability Check ---")
    plan = state.get("tactical_packet_projected", {})
    query = state.get("query", "")
    print(f"   > [MSG IN] Received Projected Tactical Packet:")
    for i, s in enumerate(plan.get('payload', [])):
        print(f"       [Stable Fact Set {i+1}]: {s[:150].strip()}...")
    
    if not plan.get("is_stable", False):
        print(f"   > [CTHA] STABILITY FAILURE: Alignment Score {plan.get('alignment_score', 0)}")
        return {"strategic_packet": "STABILITY_FAILURE"}
    
    facts_str = "\n\n".join(plan.get("payload", []))
    # Identical base instruction for both TH and CTHA
    base_prompt = f"Synthesis of evidence into a singular stable statement. Summarize {query} based on provided facts. CONSTRAINTS: One concise paragraph. No markdown. Neutral tone."
    
    # Standardized Strategic Prompt (CTHA wrapper)
    prompt = (
        "ROLE: Strategic Coordinator\n"
        f"AUTHORITY: {base_prompt}\n"
        "COMMUNICATION: RECEIVE fact set. SEND structured summary.\n"
        f"EVIDENCE:\n{facts_str}"
    )
    
    print(f"   > [CTHA] Drafting Policy-Aligned Strategic Statement...")
    response = llm.invoke(prompt)
    draft = response.content if hasattr(response, 'content') else str(response)
    print(f"   > [MSG OUT] Passing Strategic Packet to Institutional:\n       {draft.strip()}")
    return {"strategic_packet": draft}

def ctha_institutional_agent(state: AgentState) -> Dict:
    """
    ROLE: Institutional Layer - Policy alignment and final manifold projection.
    AUTHORITY SCOPE:
    - MAY: Neutralize structural noise, enforce final output constraints.
    - MAY NOT: Introduce new factual content.
    """
    print("\n--- [CTHA] Institutional Manifold: Final Policy Enforcement ---")
    draft = state.get("strategic_packet", "")
    print(f"   > [MSG IN] Received Strategic Packet:\n       {draft.strip()}")
    
    if "STABILITY_FAILURE" in draft:
        return {"final_answer": "ERROR: Strategic stability failure detected. Requesting Arbiter review."}

    # PMpol Projection: Force Policy Adherence
    final_output, noise_count = PMpol(draft)
    
    print(f"   > [FLOW] Policy Enforcement: Neutralized {noise_count} structural manifold violations.")
    print(f"   > [MSG OUT] Final Policy-Aligned Report ready:\n       {final_output.strip()}")
    return {
        "final_answer": final_output,
        "manifold_distance": noise_count
    }
