import arxiv
from app.utils.logger import log
import asyncio

async def search_arxiv(query: str) -> list[dict]:
    """
    Searches Arxiv for research papers.
    Returns title, authors, abstract, published date, and pdf url.
    """
    log.info(f"Arxiv tool executing for query: {query}")
    try:
        def run_arxiv():
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=2,
                sort_by=arxiv.SortCriterion.Relevance
            )
            return list(client.results(search))
            
        docs = await asyncio.to_thread(run_arxiv)
        return [{
            "title": d.title, 
            "url": d.entry_id, 
            "content": d.summary, 
            "source": "Research Papers (Arxiv)", 
            "authors": ", ".join([a.name for a in d.authors]),
            "published": d.published.strftime("%Y-%m-%d")
        } for d in docs]
    except Exception as e:
        log.error(f"Arxiv Search failed: {e}")
        raise e
