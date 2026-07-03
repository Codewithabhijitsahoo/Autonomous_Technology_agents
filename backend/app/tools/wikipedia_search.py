import wikipedia
from app.utils.logger import log
import asyncio

async def search_wikipedia(query: str) -> list[dict]:
    """
    Searches Wikipedia and extracts title, summary, and URL.
    """
    log.info(f"Wikipedia tool executing for query: {query}")
    try:
        # Set a custom user agent to prevent Wikipedia from blocking the request
        wikipedia.set_user_agent("DeepResearchAgent/1.0 (https://example.com; admin@example.com)")
        
        def run_wiki():
            results = wikipedia.search(query, results=2)
            docs = []
            for res in results:
                try:
                    page = wikipedia.page(res, auto_suggest=False)
                    docs.append({
                        "title": page.title,
                        "url": page.url,
                        "content": page.summary[:1500],
                        "source": "Wikipedia"
                    })
                except Exception:
                    continue
            return docs
            
        docs = await asyncio.to_thread(run_wiki)
        return docs
    except Exception as e:
        log.error(f"Wikipedia Search failed: {e}")
        raise e
