from tools.web_search import search_web
from state.schema import AgentState

def search_agent(state: AgentState) -> AgentState:
    query = state.get("query", "")
    retries = state.get("retry_count", 0)
    
    print(f"--- SEARCHING (Attempt {retries + 1}) ---")
    results = search_web(query)

    return {
        **state, 
        "search_results": results, 
        "retry_count": retries + 1
    }