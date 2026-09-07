from tools.research_tools import query_ollama
from tools.competitor_research import competitor_research
from tools.problem_research import problem_research
from tools.pricing_research import pricing_research
from tools.opportunity_scorer import opportunity_scorer
from memory.database import Database

from models.task import Task

class ResearchAgent:
    def __init__(self):
        self.db = Database()

    def run(self, task_or_input) -> dict:
        if isinstance(task_or_input, Task):
            task_id = task_or_input.task_id
            goal = task_or_input.input_data
        else:
            task_id = 0
            goal = str(task_or_input)

        if not goal:
            return {"status": "error", "agent": "ResearchAgent", "task_id": task_id, "result": None, "errors": "No input_data provided"}
        
        # Step 1: Brainstorm commercial concept prioritizing B2B / SaaS / Workflow automation
        initial_prompt = f"""
        Given the following research goal:
        '{goal}'
        
        Prioritize REAL REVENUE OPPORTUNITIES in these categories:
        - B2B SaaS
        - Micro-SaaS
        - AI / Business Workflow Automation
        - Document Automation
        - Developer Tools
        - Education tools with PROVEN willingness to pay
        
        AVOID:
        - Generic chatbots or generic AI writers
        - Generic to-do / expense apps without B2B buyer model
        - Copycat social networks
        - Speculative revenue ideas with no clear buyer
        
        Identify one specific commercial product idea fitting these rules.
        Return ONLY the product name/concept on line 1, and the target paying customer persona on line 2.
        """
        
        concept_response_text = query_ollama(initial_prompt)
        
        lines = concept_response_text.strip().split('\n')
        product_idea = lines[0] if len(lines) > 0 else goal
        problem = lines[1] if len(lines) > 1 else goal
        
        # Step 2: Run Research Tools
        problem_evidence = problem_research(problem)
        competitors = competitor_research(product_idea)
        pricing = pricing_research(product_idea)
        
        # Step 3: Score Opportunity (REVENUE SCORE 0-100)
        research_data = f"Product: {product_idea}\nProblem Evidence:\n{problem_evidence}\nCompetitors:\n{competitors}\nPricing:\n{pricing}"
        score_evaluation = opportunity_scorer(research_data)
        
        # Step 4: Final Formatting with 7 Commercial Questions & Data Tags
        final_prompt = f"""
        You are a commercial business research AI agent.
        Format the final output strictly according to the template below.
        CRITICAL: Never invent revenue figures. Tag every data point explicitly as [VERIFIED DATA], [ESTIMATE], or [UNKNOWN].
        
        Data Input:
        Product Idea: {product_idea}
        Target Customer/Goal: {goal}
        Problem Evidence: {problem_evidence}
        Competitors: {competitors}
        Pricing: {pricing}
        Scores: {score_evaluation}
        
        OUTPUT TEMPLATE:

        PRODUCT OPPORTUNITY & COMMERCIAL HIGHLIGHTS
        -------------------
        Product: {product_idea}
        Target Category: [B2B SaaS / Workflow Automation / Developer Tools / Micro-SaaS]
        Target Customer: 

        COMMERCIAL ANALYSIS (7 MANDATORY QUESTIONS)
        -------------------
        1. WHO PAYS? [Tag] [Detailed answer]
        2. WHY DO THEY PAY? [Tag] [Detailed answer]
        3. HOW MUCH DO THEY PAY? [Tag] [Price point]
        4. HOW OFTEN DO THEY PAY? [Tag] [Subscription frequency - MRR/ARR]
        5. WHAT PROBLEM ARE WE SOLVING? [Tag] [Pain point description]
        6. WHY WOULD THEY CHOOSE US? [Tag] [Competitive advantage / MVP simplicity]
        7. HOW DO WE REACH THEM? [Tag] [Acquisition channel]

        MARKET METRICS & DATA TAGS
        -------------------
        Existing Customer Spending: [Tag] [Details]
        Existing Competitors: [Tag] [List]
        Competitor Pricing: [Tag] [Observed prices]
        Customer Urgency: [Tag] [High/Medium/Low]
        Willingness to Pay: [Tag] [High/Medium/Low]
        Recurring Revenue Potential: [Tag] [High/Medium/Low]
        Estimated MVP Dev Time: [Tag] [e.g. 1-2 weeks]
        Customer Acquisition Difficulty: [Tag] [Easy/Moderate/Hard]

        REVENUE SCORE (0-100)
        -------------------
        {score_evaluation}

        FINAL RECOMMENDATION
        -------------------
        RECOMMENDATION: [BUILD NOW / INVESTIGATE FURTHER / REJECT]

        Executive Summary & Justification:
        """
        
        result = query_ollama(final_prompt)
        
        # Save to memory
        self.db.save_research(goal, {"product": product_idea, "result": result})
        
        return {
            "status": "success",
            "agent": "ResearchAgent",
            "task_id": task_id,
            "result": result,
            "artifacts": [],
            "errors": []
        }
