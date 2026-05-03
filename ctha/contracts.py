from typing import Dict, List, Any

def PMsum(packet: List[Dict]) -> List[Dict]:
    """
    Manifold Projection for Summary.
    """
    projected = []
    noise_keywords = ["access denied", "403 forbidden", "404 not found", "robot check"]
    
    for item in packet:
        content = item.get("content", "").lower()
        if any(kw in content for kw in noise_keywords):
            continue
        if len(content) < 400:
            continue
            
        projected.append({
            "url": item.get("url", ""),
            "content": item.get("content", "")[:2000],
            "density": "VALIDATED"
        })
    return projected

def PMplan(summaries: List[str]) -> Dict[str, Any]:
    """
    Manifold Projection for Plan.
    """
    if not summaries:
        return {"fact_count": 0, "payload": [], "is_stable": False}
    
    has_target = any(any(w in s.lower() for w in ["war", "conflict", "news", "fusion", "ukraine"]) for s in summaries)
    
    return {
        "fact_count": len(summaries),
        "payload": summaries,
        "is_stable": (len(summaries) >= 2) and has_target,
        "manifold_id": "V1_STABLE"
    }

def PMpol(draft: str) -> str:
    """
    Final Policy Manifold (REVISED: STRICT CONCISENESS).
    POLICY: The final output MUST be a single, unified paragraph.
    """
    if not draft: return ""
    
    # Remove all headers, bullet points, and extra newlines
    import re
    clean = re.sub(r'\*+', '', draft) # Remove bold/bullets
    clean = re.sub(r'#+', '', clean) # Remove headers
    
    # Merge all lines into one paragraph
    lines = [line.strip() for line in clean.split('\n') if line.strip()]
    merged = " ".join(lines)
    
    # Ensure it's not too long (Policy truncation)
    return merged[:1000] + "..." if len(merged) > 1000 else merged

def validate_contract(state: Dict) -> bool:
    plan = state.get("tactical_packet_projected", {})
    return plan.get("is_stable", False)