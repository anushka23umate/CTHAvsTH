from typing import Dict, List
try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        # If neither works, we'll define a dummy to avoid crash before synced data check
        DDGS = None

import requests
from bs4 import BeautifulSoup
from state.schema import AgentState

def reflex_agent(state: AgentState) -> Dict:
    """
    LAYER: REFLEX (Perception)
    Responsibility: Raw data acquisition.
    Constraint: If data is already provided in state (Synced Run), skip search.
    """
    existing_data = state.get("reflex_packet", [])
    if existing_data:
        print(f"\n[LAYER: REFLEX] Using pre-provided synced data ({len(existing_data)} sources).")
        return {"reflex_packet": existing_data}

    query = state.get("query", "General Research")
    print(f"\n[LAYER: REFLEX] Fetching LIVE Data (Attempt {state.get('retry_count', 0) + 1})")
    
    results = []
    try:
        with DDGS() as ddgs:
            print("   > [DDGS] Attempting search...")
            search_results = list(ddgs.text(query, max_results=5))
            print(f"   > [DDGS] Found {len(search_results)} results.")
            
            for r in search_results:
                url = r.get('href')
                try:
                    print(f"   > Attempting scrape: {url}")
                    resp = requests.get(url, timeout=10)
                    resp.raise_for_status()
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    # Extract text content
                    text = ' '.join([p.text for p in soup.find_all('p')])
                    results.append({
                        "url": url,
                        "content": text[:5000] # Cap size for demo
                    })
                    print(f"   > Data acquired. Size: {len(text[:5000])} characters.")
                except Exception as scrape_err:
                    # Supressing print to keep logs focused on Inter-layer communication
                    # print(f"--- [SCRAPER] Failed to scrape {url}: {str(scrape_err)} ---")
                    # Still keep the snippet from DDGS if scrape fails
                    results.append({"url": url, "content": r.get('body', '')})
                    
    except Exception as e:
        print(f"--- [REFLEX ERROR] Search failed: {str(e)} ---")
        
    return {"reflex_packet": results}
