from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the internet for relevant information.
    Return useful sources and snippets.
    """
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return "No results found."
        
        formatted_results = []
        for r in results:
            formatted_results.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nSource: {r.get('href')}")
        
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error performing web search: {str(e)}"
