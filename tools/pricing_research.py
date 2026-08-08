from tools.web_search import web_search
import ollama

def pricing_research(product_category: str) -> str:
    """
    Find actual market pricing.
    Clearly distinguish between verified prices and estimates.
    """
    search_query = f"{product_category} software pricing cost"
    search_results = web_search(search_query, max_results=5)
    
    prompt = f"""
    Based on the following search results for pricing of '{product_category}':
    
    {search_results}
    
    Identify actual market pricing.
    Format your response to clearly state:
    1. Observed market prices
    2. Sources
    3. Estimated price for our product (based on the market)
    
    IMPORTANT: Clearly distinguish between verified prices from the sources and your estimates. Do NOT invent prices. If you cannot find verified prices, state "Not verified".
    """
    
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"]
