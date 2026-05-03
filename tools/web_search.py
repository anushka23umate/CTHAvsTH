import warnings
# GLOBAL WARNING SUPPRESSION
warnings.simplefilter("ignore") 

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

from googlesearch import search as gsearch
import time
import random

def search_web(query, num_results=5):
    """
    Production-grade Hybrid Search.
    Uses 'ddgs' primary import to avoid warnings and falls back to Google.
    """
    results = []
    
    # 1. Try DuckDuckGo (via the new ddgs import if possible)
    try:
        print(f"   > [DDGS] Attempting search...")
        with DDGS(timeout=30) as ddgs:
            # We try a broader query if it's too specific
            search_query = query.replace(" May ", " ")
            ddg_gen = ddgs.text(search_query, max_results=num_results)
            if ddg_gen:
                for r in ddg_gen:
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "body": r.get("body", "")
                    })
                if results: 
                    print(f"   > [DDGS] Found {len(results)} results.")
                    return results
    except Exception as e:
        print(f"   > [DDGS] Connection issue: {e}")

    # 2. Try Google Search Fallback
    try:
        print(f"   > [GOOGLE] Attempting fallback...")
        # advanced=True returns objects with titles and descriptions
        g_results = gsearch(query, num_results=num_results, advanced=True, sleep_interval=2)
        for r in g_results:
            results.append({
                "title": r.title,
                "url": r.url,
                "body": r.description
            })
        
        if results:
            print(f"   > [GOOGLE] Found {len(results)} results.")
            return results
    except Exception as e:
        print(f"   > [GOOGLE] Failed: {e}")

    return []