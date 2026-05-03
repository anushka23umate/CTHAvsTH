from tools.scraper import scrape_url
from state.schema import AgentState


def scrape_agent(state: AgentState) -> AgentState:
    results = state["search_results"]

    scraped_data = []
    for r in results:
        content = scrape_url(r["url"])
        scraped_data.append({
            "url": r["url"],
            "content": content
        })

    return {**state, "scraped_data": scraped_data}