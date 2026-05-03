from config.llm import get_llm
from state.schema import AgentState

llm = get_llm()

def summarize_agent(state: AgentState) -> AgentState:
    data = state.get("scraped_data", [])

    summaries = []
    for d in data:
        content = d.get('content', '')
        if not content: continue
        
        prompt = f"""
        You are a STRICT information extraction system.

        TASK:
        Extract only high-value factual insights from the content.

        RULES:
        - Output EXACTLY 5 bullet points
        - Each bullet = max 20 words
        - No explanations, no fluff
        - No repetition
        - Ignore opinions, ads, or irrelevant text
        - Focus on scientific, technical, or measurable facts

        OUTPUT FORMAT:
        - point 1
        - point 2
        - point 3
        - point 4
        - point 5

        CONTENT:
            {content}
            """
        response = llm.invoke(prompt)
        summary = response.content if hasattr(response, 'content') else str(response)
        summaries.append(summary)

    return {**state, "summaries": summaries}