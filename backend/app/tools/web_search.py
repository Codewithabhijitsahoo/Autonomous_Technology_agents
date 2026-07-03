import os
from duckduckgo_search import DDGS
from langchain_community.tools.tavily_search import TavilySearchResults
from app.utils.logger import log
import asyncio

async def search_web(query: str) -> list[dict]:
    """
    Searches the web using Tavily if an API key is present, otherwise falls back to DuckDuckGo.
    Returns standardized results.
    """
    log.info(f"Web Search tool executing for query: {query}")
    try:
        tavily_key = os.getenv("TAVILY_API_KEY")
        if tavily_key:
            tool = TavilySearchResults(max_results=3, tavily_api_key=tavily_key)
            results = await tool.ainvoke({"query": query})
            return [{"title": r.get("title", ""), "url": r.get("url", ""), "content": r.get("content", ""), "source": "Web Search (Tavily)"} for r in results]
        else:
            def run_ddg():
                ddgs = DDGS()
                return list(ddgs.text(query, max_results=3))
            results = await asyncio.to_thread(run_ddg)
            return [{"title": r.get("title", ""), "url": r.get("href", ""), "content": r.get("body", ""), "source": "Web Search (DDG)"} for r in results]
    except Exception as e:
        log.error(f"Web Search failed: {e}")
        raise e
