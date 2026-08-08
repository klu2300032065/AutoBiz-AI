from tools.web_search import web_search
import ollama

def competitor_research(product_idea: str) -> str:
    """
    Find existing products/services solving the same problem.
    Identify competitor names, actual pricing when available, and their main features.
    """
    search_query = f"competitors alternatives to {product_idea} software"
    search_results = web_search(search_query, max_results=5)
    
    prompt = f"""
    Based on the following search results for competitors of '{product_idea}':
    
    {search_results}
    
    Extract a list of competitors. For each, identify:
    1. Competitor Name
    2. Main Features
    3. Pricing (if mentioned, otherwise say "Not verified")
    4. Source URL
    
    Do NOT invent competitors or pricing. Only use the provided search results.
    If no competitors are found in the results, state that.
    """
    
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"]
