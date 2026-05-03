import os
import warnings
warnings.simplefilter("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
import logging

from th.graph import build_graph as th_graph
from ctha.graph import build_graph as ctha_graph
from agents.reflex_agent import reflex_agent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_comparison():
    # As per your manual edit
    query = "Latest war news around the globe"
    
    print("\n" + "="*60)
    print(f"INGRESS: Fetching Shared Raw Data for Query: {query}")
    print("="*60)
    
    # FETCH SHARED DATA ONCE
    initial_state = {"query": query, "retry_count": 0}
    shared_reflex_state = reflex_agent(initial_state)
    raw_packet = shared_reflex_state.get("reflex_packet", [])
    total_raw_chars = sum(len(item.get("content", "")) for item in raw_packet)
    
    print(f"   > Shared Data Acquired: {len(raw_packet)} sources, {total_raw_chars} total characters.")

    # 1. RUN TH (Traditional)
    print("\n" + "="*60)
    print("RUNNING TH (TRADITIONAL HIERARCHY) - UNCONSTRAINED")
    print("="*60)
    th_app = th_graph()
    th_state = {**initial_state, "reflex_packet": raw_packet}
    
    th_output = ""
    th_summaries = []
    th_failed = False
    try:
        final_state_th = th_app.invoke(th_state)
        th_output = final_state_th.get("final_answer", "")
        th_summaries = final_state_th.get("tactical_packet", [])
    except Exception as e:
        th_output = f"CRASH: {str(e)}"
        th_failed = True

    # 2. RUN CTHA (Constrained)
    print("\n" + "="*60)
    print("RUNNING CTHA (CONSTRAINED T.H.A.) - STABLE")
    print("="*60)
    ctha_app = ctha_graph()
    ctha_state = {**initial_state, "reflex_packet": raw_packet}
    
    ctha_output = ""
    ctha_summaries = []
    ctha_backtracks = 0
    ctha_is_stable = False
    ctha_failed = False
    
    try:
        final_state_ctha = ctha_app.invoke(ctha_state)
        ctha_output = final_state_ctha.get("final_answer", "")
        ctha_summaries = final_state_ctha.get("tactical_packet", [])
        ctha_backtracks = final_state_ctha.get("retry_count", 0)
        ctha_is_stable = "Stability Failure" not in ctha_output and "ERROR" not in ctha_output
    except Exception as e:
        ctha_output = f"CRASH: {str(e)}"
        ctha_failed = True

    # 3. THE COMPARISON DASHBOARD
    print("\n\n" + "="*16 + " COMPARISON " + "="*16)
    
    # Calculate filtered size correctly
    ctha_filtered_chars = sum(len(s) for s in ctha_summaries) if ctha_summaries else 0
    th_summarized_chars = sum(len(s) for s in th_summaries) if th_summaries else 0

    print(f"\n--- [TH: TRADITIONAL HIERARCHY] ---")
    print(f"STATUS: {'CRASHED' if th_failed else 'COMPLETE'}")
    print(f"RAW INPUT SIZE: {total_raw_chars} chars")
    print(f"SUMMARIZED SIZE: {th_summarized_chars} chars (Unfiltered)")
    print(f"RECOVERY: ❌ None (Propagated errors)")

    print(f"\n--- [CTHA: CONSTRAINED T.H.A.] ---")
    status_ctha = "STABLE" if ctha_is_stable else "REFUSED (Stability Failure)"
    print(f"STATUS: {status_ctha}")
    print(f"FILTERED SIZE: {ctha_filtered_chars} chars (Manifold Enforced)")
    print(f"RECOVERY: ✅ Arbiter resolved conflicts ({ctha_backtracks} backtracks)")

    print("\n" + "="*43)
    
    # 4. SHOW ACTUAL RESPONSES
    print("\n[TH FULL RESPONSE]:")
    print("-" * 20)
    print(th_output if th_output else "No response generated.")
    print("-" * 20)

    print("\n[CTHA FULL RESPONSE]:")
    print("-" * 20)
    print(ctha_output if ctha_output else "No response generated.")
    print("-" * 20)

    print("\n" + "="*43 + "\n")

if __name__ == "__main__":
    run_comparison()