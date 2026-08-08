import ollama
from tools.competitor_research import competitor_research
from tools.problem_research import problem_research
from tools.pricing_research import pricing_research
from tools.opportunity_scorer import opportunity_scorer
from memory.database import Database

class ResearchAgent:
    def __init__(self):
        self.db = Database()

    def run(self, goal: str) -> str:
        # Step 1: Brainstorm basic concept if it's a broad goal, or use goal as concept
        initial_prompt = f"""
        Given the following research goal:
        '{goal}'
        
        Identify one specific software product idea that fits this goal.
        Return ONLY the product name/concept on one line, and the core problem it solves on the next line.
        """
        
        concept_response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": initial_prompt}]
        )
        
        lines = concept_response["message"]["content"].strip().split('\n')
        product_idea = lines[0] if len(lines) > 0 else goal
        problem = lines[1] if len(lines) > 1 else goal
        
        # Step 2: Run Research Tools
        problem_evidence = problem_research(problem)
        competitors = competitor_research(product_idea)
        pricing = pricing_research(product_idea)
        
        # Step 3: Score Opportunity
        research_data = f"Product: {product_idea}\nProblem Evidence:\n{problem_evidence}\nCompetitors:\n{competitors}\nPricing:\n{pricing}"
        score_evaluation = opportunity_scorer(research_data)
        
        # Step 4: Final Formatting
        final_prompt = f"""
        You are a business research AI agent.
        Format the final output strictly according to the following template.
        Do NOT invent any data. If something is missing or unverified, state "Not verified".
        
        Data:
        Product Idea: {product_idea}
        Problem: {problem}
        Target Customer: Based on '{goal}'
        Problem Evidence: {problem_evidence}
        Competitors: {competitors}
        Pricing: {pricing}
        Scores: {score_evaluation}
        
        OUTPUT FORMAT:

        PRODUCT OPPORTUNITY
        -------------------
        Product:
        Problem:
        Target customer:

        REAL MARKET EVIDENCE
        -------------------
        Evidence:
        Sources:

        COMPETITORS
        -------------------
        Competitor:
        Features:
        Pricing:
        Source:

        PRICING
        -------------------
        Observed market prices:
        Source:
        Estimated price for our product:

        OPPORTUNITY SCORE
        -------------------
        Problem severity: X/10
        Demand: X/10
        Competition: X/10
        Willingness to pay: X/10
        Development difficulty: X/10
        Scalability: X/10

        FINAL SCORE: X/100

        RECOMMENDATION
        -------------------
        Build / Don't Build / Needs More Research

        Reason:
        """
        
        final_response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": final_prompt}]
        )
        
        result = final_response["message"]["content"]
        
        # Save to memory
        self.db.save_research(goal, {"product": product_idea, "result": result})
        
        return result
