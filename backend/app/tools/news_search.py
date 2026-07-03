from duckduckgo_search import DDGS
from app.utils.logger import log
import asyncio

async def search_news(query: str) -> list[dict]:
    """
    Searches latest news using DuckDuckGo News search.
    """
    log.info(f"News Search tool executing for query: {query}")
    try:
        def run_news():
            ddgs = DDGS()
            return list(ddgs.news(query, max_results=3))
            
        results = await asyncio.to_thread(run_news)
        return [{"title": r.get("title", ""), "url": r.get("url", ""), "content": r.get("body", ""), "source": "News Search", "date": r.get("date", "")} for r in results]
    except Exception as e:
        log.error(f"News Search failed: {e}")
        raise e
