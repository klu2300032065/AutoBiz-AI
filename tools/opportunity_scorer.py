import ollama

def opportunity_scorer(data: str) -> str:
    """
    Score the opportunity based on collected data.
    """
    prompt = f"""
    Based on the following market research data:
    
    {data}
    
    Score this product opportunity on a scale of 0-10 for the following criteria:
    - Problem severity
    - Demand
    - Competition
    - Willingness to pay
    - Development difficulty
    - Scalability
    
    Then provide a Final Score out of 100 (sum of the 6 scores scaled, or just a holistic 0-100 score).
    
    For EACH score, provide a brief 1-sentence explanation of why you gave that score based on the evidence.
    
    Format:
    Problem severity: X/10 - [explanation]
    Demand: X/10 - [explanation]
    Competition: X/10 - [explanation]
    Willingness to pay: X/10 - [explanation]
    Development difficulty: X/10 - [explanation]
    Scalability: X/10 - [explanation]
    
    FINAL SCORE: X/100
    """
    
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"]
