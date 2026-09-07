from tools.research_tools import query_ollama

def opportunity_scorer(data: str) -> str:
    """
    Calculate structured REVENUE SCORE (0-100) based on real commercial opportunity metrics.
    """
    prompt = f"""
    Based on the following market research data:
    
    {data}
    
    Evaluate and score this commercial opportunity on a 0-100 scale using the weighted REVENUE SCORE formula:
    
    1. Willingness to Pay & Existing Spending (0-25 pts)
       - Do customers/businesses already spend money on existing solutions?
    2. Customer Urgency & Problem Severity (0-20 pts)
       - Is this a painful, urgent problem or just a nice-to-have?
    3. Recurring Revenue Potential (0-20 pts)
       - Can this support monthly/annual recurring subscription revenue (MRR/ARR)?
    4. MVP Feasibility & Dev Simplicity (0-15 pts)
       - Can we build a working MVP quickly with Python/FastAPI/React?
    5. Customer Acquisition Feasibility (0-10 pts)
       - Is there a clear, low-friction channel to reach paying buyers (b2b outreach, forums, dev communities)?
    6. Low Competition / Differentiated Value (0-10 pts)
       - Is the market uncrowded or are existing solutions overpriced/poorly designed?

    CRITICAL RULES:
    - Never invent numbers.
    - Clearly tag evidence for each criterion as [VERIFIED DATA], [ESTIMATE], or [UNKNOWN].
    - Calculate REVENUE SCORE = Sum of all 6 scores (Max 100).
    
    Format:
    Willingness to Pay & Existing Spending: X/25 - [Tag] [Explanation]
    Customer Urgency & Problem Severity: X/20 - [Tag] [Explanation]
    Recurring Revenue Potential: X/20 - [Tag] [Explanation]
    MVP Feasibility & Dev Simplicity: X/15 - [Tag] [Explanation]
    Customer Acquisition Feasibility: X/10 - [Tag] [Explanation]
    Low Competition / Differentiated Value: X/10 - [Tag] [Explanation]
    
    REVENUE SCORE: X/100
    RECOMMENDATION: [BUILD NOW / INVESTIGATE FURTHER / REJECT]
    """
    
    return query_ollama(prompt)

