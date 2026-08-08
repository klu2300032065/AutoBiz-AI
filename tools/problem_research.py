from tools.web_search import web_search
import ollama

def problem_research(problem: str) -> str:
    """
    Search for evidence that users actually experience the problem.
    Look for discussions, reviews, forums, articles, and other legitimate sources.
    """
    search_query = f"\"{problem}\" site:reddit.com OR site:quora.com OR forums"
    search_results = web_search(search_query, max_results=5)
    
    prompt = f"""
    Based on the following search results about the problem: '{problem}'
    
    {search_results}
    
    Summarize the real market evidence that users actually experience this problem.
    Provide the summary and list the source URLs.
    Do not invent evidence. If no strong evidence is found, state "Not verified".
    """
    
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"]
