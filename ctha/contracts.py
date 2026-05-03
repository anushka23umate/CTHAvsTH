from typing import Dict, List, Any

def PMsum(packet: List[Dict]) -> List[Dict]:
    """
    Manifold Projection for Summary.
    REJECTION: Strictly filter out administrative noise (403, 404, robots).
    """
    projected = []
    # Removed 'cookies' and 'subscribe' to allow more news sources in the demo
    noise_keywords = [
        "access denied", "403 forbidden", "404 not found", 
        "robot check", "please enable javascript"
    ]
    
    for item in packet:
        content = item.get("content", "").lower()
        if any(kw in content for kw in noise_keywords):
            continue
        if len(content) < 400: # Slightly lower threshold for 'Density'
            continue
            
        projected.append({
            "url": item.get("url", ""),
            "content": item.get("content", "")[:2500], # Increased limit slightly
            "density": "VALIDATED"
        })
    return projected

def PMplan(summaries: List[str]) -> Dict[str, Any]:
    """
    Manifold Projection for Plan.
    """
    if not summaries:
        return {"fact_count": 0, "payload": [], "is_stable": False}
    
    # Check for general relevance to war/conflict/news
    has_target = any(any(w in s.lower() for w in ["war", "conflict", "news", "fusion", "ukraine", "russia"]) for s in summaries)
    
    return {
        "fact_count": len(summaries),
        "payload": summaries,
        "is_stable": (len(summaries) >= 2) and has_target,
        "manifold_id": "V1_STABLE"
    }

def PMpol(draft: str) -> str:
    """
    Final Policy Manifold.
    """
    if not draft: return ""
    blocks = draft.split('\n\n')
    unique_blocks = []
    seen = set()
    for b in blocks:
        clean_b = b.strip()
        if clean_b and clean_b[:100] not in seen:
            unique_blocks.append(clean_b)
            seen.add(clean_b[:100])
    return "\n\n".join(unique_blocks)

def validate_contract(state: Dict) -> bool:
    plan = state.get("tactical_packet_projected", {})
    return plan.get("is_stable", False)