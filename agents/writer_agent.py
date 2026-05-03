from config.llm import get_llm
from state.schema import AgentState    

llm = get_llm()

def writer_agent(state: AgentState) -> AgentState:
    summaries = state.get("summaries", [])
    query = state.get("query", "")

    prompt = f"""
    You are a professional writer. Based on the following research summaries, provide a comprehensive answer to the user's query.
    
    User Query: {query}

    Research Summaries:
    {" ".join(summaries)}

    Answer:"""

    response = llm.invoke(prompt)
    final_answer = response.content if hasattr(response, 'content') else str(response)

    return {**state, "final_answer": final_answer}