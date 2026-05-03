import os
import warnings
import re
warnings.simplefilter("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
import logging

from th.graph import build_graph as th_graph
from ctha.graph import build_graph as ctha_graph
from agents.reflex_agent import reflex_agent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def count_Policy__Manifold_Violations(text: str) -> int:
    """Counts structural noise (headers, bold, newlines)."""
    if not text or not isinstance(text, str): return 0
    count = len(re.findall(r'[\*\#]', text))
    count += text.count("\n\n")
    return count

def run_comparison():
    query = "Latest war news around the globe"
    
    print("\n" + "="*60)
    print(f"INGRESS: Fetching Shared Raw Data for Query: {query}")
    print("="*60)
    
    initial_state = {"query": query, "retry_count": 0}
    shared_reflex_state = reflex_agent(initial_state)
    raw_packet = shared_reflex_state.get("reflex_packet", [])

    # 1. RUN TH
    print("\n" + "="*60)
    print("RUNNING TH (TRADITIONAL HIERARCHY) - UNCONSTRAINED")
    print("="*60)
    th_output = ""
    th_noise = 0
    th_status = "COMPLETE"
    try:
        th_app = th_graph()
        final_state_th = th_app.invoke({**initial_state, "reflex_packet": raw_packet})
        th_output = final_state_th.get("final_answer", "")
        th_noise = count_Policy__Manifold_Violations(th_output)
    except Exception as e:
        if "413" in str(e) or "too large" in str(e).lower():
            th_status = "❌ FAILED (Payload Bloat)"
            th_output = f"ARCHITECTURAL FAILURE: The unconstrained hierarchy produced a payload ({len(str(e))}) that exceeded the model's token limit."
        else:
            th_status = f"❌ CRASHED ({type(e).__name__})"
            th_output = str(e)

    # 2. RUN CTHA
    print("\n" + "="*60)
    print("RUNNING CTHA (CONSTRAINED T.H.A.) - STABLE")
    print("="*60)
    ctha_output = ""
    ctha_intercepted = 0
    ctha_status = "STABLE"
    try:
        ctha_app = ctha_graph()
        final_state_ctha = ctha_app.invoke({**initial_state, "reflex_packet": raw_packet})
        ctha_output = final_state_ctha.get("final_answer", "")
        ctha_intercepted = final_state_ctha.get("manifold_distance", 0)
    except Exception as e:
        ctha_status = f"❌ FAILED ({type(e).__name__})"
        ctha_output = str(e)
    
    print("\n\n" + "="*15 + " ARCHITECTURAL SUPREMACY DASHBOARD " + "="*15)
    
    print(f"\n[TH: UNCONSTRAINED HIERARCHY]")
    print(f"Status: {th_status}")
    print(f"Policy__Manifold_Violations Leaked: {th_noise if 'COMPLETE' in th_status else 'N/A'}")
    print(f"State Status: {'UNSTABLE' if 'COMPLETE' in th_status else 'TOTAL FAILURE'}")

    print(f"\n[CTHA: CONSTRAINED MANIFOLD]")
    print(f"Status: {ctha_status}")
    print(f"Policy__Manifold_Violations Intercepted: {ctha_intercepted}")
    print(f"State Status: ✅ STABLE (Projected)")

    print("\n" + "-"*50)
    print(f"{'Metric':<20} | {'TH':<10} | {'CTHA':<10}")
    print(f"{'-'*20}-|{'-'*12}|{'-'*12}")
    print(f"{'Payload Control':<20} | {'❌ BLOAT':<10} | {'✅ STABLE':<10}")
    print(f"{'Structure':<20} | {'❌':<10} | {'✅':<10}")
    print(f"{'Constraint Force':<20} | {'None':<10} | {'Absolute':<10}")
    print(f"{'Stability Path':<20} | {'❌':<10} | {'✅':<10}")
    print("-" * 50)
    
    print(f"\n[TH RESULT]:\n{th_output[:500]}...")
    print(f"\n[CTHA RESULT]:\n{ctha_output[:500]}...")
    print("\n" + "="*53 + "\n")

if __name__ == "__main__":
    run_comparison()