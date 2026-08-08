import os
from dotenv import load_dotenv
from agents.research_agent import ResearchAgent
from agents.builder_agent import BuilderAgent

def main():
    load_dotenv()
    
    print("Welcome to AutoBiz AI")
    print("1. Research Mode")
    print("2. Build Mode")
    
    choice = input("Select a mode (1 or 2): ").strip()
    
    if choice == "1":
        agent = ResearchAgent()
        goal = input("What should the agent research? (Press Enter to use default test query)\n")
        if not goal.strip():
            goal = "Find software products that Indian college students would realistically pay for."
            print(f"Using test query: '{goal}'")
        
        print("\nAgent is researching... This may take a few minutes as it browses the web.\n")
        result = agent.run(goal)
        print("\n===== RESEARCH AGENT v2 =====\n")
        print(result)
        
    elif choice == "2":
        agent = BuilderAgent()
        
        default_spec = """
Product: Student Expense Tracker
Problem: College students need a simple way to track daily expenses.
Features: Add expense, Delete expense, Categories, Monthly total, Dashboard, Expense history, Responsive UI.
Technology: React + Vite, FastAPI, SQLite
"""
        spec = input("Provide product specification (Press Enter to use default test spec):\n")
        if not spec.strip():
            spec = default_spec
            print(f"Using default specification:{spec}")
            
        print("\nBuilder Agent is generating the project... This will take a few minutes.\n")
        result = agent.run(spec)
        print(result)
        
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()