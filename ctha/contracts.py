from typing import Dict, List, Any, Tuple
import re

def PMsum(packet: List[Dict], max_sources: int = 4) -> List[Dict]:
    """
    Manifold Projection for Summary (Upward Message).
    Implements: Validate, Truncate k, and Sanitize.
    """
    projected = []
    noise_keywords = ["access denied", "404 not found", "captcha", "cookie policy"]
    
    # 1. Validate & Sanitize
    for item in packet:
        content = item.get("content", "")
        if not isinstance(content, str):
            content = str(content)
            
        # Remove structural noise (excessive whitespace, script tags placeholders, etc)
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Check against noise manifold
        if any(kw in content.lower() for kw in noise_keywords):
            continue
        
        if len(content) < 300: # Information density threshold
            continue
            
        projected.append({
            "url": item.get("url", ""),
            "content": content[:2000], # Truncate per source
            "status": "VALIDATED"
        })
    
    # 2. Truncate k (Temporal hierarchy constraint)
    return projected[:max_sources]

def PMplan(summaries: List[str], query: str = "") -> Dict[str, Any]:
    """
    Manifold Projection for Plan (Downward Message).
    Enforces goal alignment and stability.
    """
    if not summaries:
        return {"fact_count": 0, "payload": [], "is_stable": False, "reason": "No valid evidence"}
    
    # Check for semantic alignment with the query
    query_terms = set(re.findall(r'\w{4,}', query.lower()))
    combined_evidence = " ".join(summaries).lower()
    
    alignment_score = sum(1 for term in query_terms if term in combined_evidence)
    is_stable = alignment_score > 0 or not query_terms
    
    return {
        "fact_count": len(summaries),
        "payload": summaries,
        "is_stable": is_stable,
        "alignment_score": alignment_score,
        "state_validity": "VERIFIED" if is_stable else "UNSTABLE"
    }

def PMpol(draft: str) -> Tuple[str, int]:
    """
    Policy Manifold (Institutional Constraint).
    Neutralizes structural violations and ensures formatting compliance.
    """
    if not draft: return "", 0
    
    # Detect structural noise (e.g., markdown artifacts not requested)
    violations = len(re.findall(r'[\*\#\-\[\]]', draft))
    
    # Sanitize: Remove all markdown headers, bullets, and bolding for 'Concise Paragraph' policy
    clean = re.sub(r'[\*\#\-\[\]]', '', draft)
    clean = " ".join(clean.split()) # Normalize whitespace
    
    return clean, violations

def validate_contract(state: Dict) -> bool:
    """Arbiter-level contract validation."""
    plan = state.get("tactical_packet_projected", {})
    return plan.get("is_stable", False)