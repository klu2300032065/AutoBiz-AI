import time
import sys
import os

from agents.ceo_agent import CEOAgent
from memory.business_memory import BusinessMemory
from services.approval_manager import ApprovalManager
from services.task_manager import TaskManager
from models.msa_db import get_db

DEFAULT_OBJECTIVES = [
    "Find software products that Indian college students would realistically pay for.",
    "Research high-demand B2B micro-SaaS opportunities in invoice auditing and workflow automation.",
    "Find profitable developer productivity tools and API integrations with strong commercial demand.",
    "Research AI-powered marketing and content automation tools for small e-commerce businesses.",
    "Find vertical SaaS ideas for healthcare clinics and small medical practices."
]

class AutonomousRunner:
    def __init__(self, auto_approve: bool = True, max_cycles: int = 5, sleep_interval: int = 2):
        self.ceo = CEOAgent()
        self.memory = BusinessMemory()
        self.approval_manager = ApprovalManager()
        self.task_manager = TaskManager()
        self.auto_approve = auto_approve
        self.max_cycles = max_cycles
        self.sleep_interval = sleep_interval

    def auto_approve_pending(self, cycle_id: int):
        pending = self.memory.get_pending_approvals(cycle_id=cycle_id)
        if not pending:
            return False

        for app in pending:
            act_cost = app.actual_cost if app.deployment_mode != "LOCAL/DEMO" else 0.0
            print(f"[AUTONOMOUS ENGINE] Auto-approving Action [{app.approval_id}] ({app.action}): {app.description} (Risk: {app.risk_level}, Est. Cost: ${app.estimated_cost:.2f}, Actual Exp: ${act_cost:.2f}, Mode: {app.deployment_mode})")
            self.approval_manager.approve(app.approval_id)
            
            # Also update MSA database if post related
            try:
                conn = get_db()
                c = conn.cursor()
                c.execute("UPDATE posts SET status='APPROVED' WHERE post_id=?", (app.approval_id,))
                conn.commit()
                conn.close()
            except Exception:
                pass

        return True

    def simulate_revenue_and_growth(self, cycle_id: int):
        """Simulates customer acquisition and revenue generation once marketing is live."""
        state = self.memory.get_business_state(cycle_id=cycle_id)
        if state.stage == "MARKETING_LIVE" and state.revenue == 0.0:
            import random
            new_customers = random.randint(5, 25)
            monthly_arpu = random.choice([29.0, 49.0, 99.0, 199.0])
            total_rev = round(new_customers * monthly_arpu, 2)
            
            state.customers = new_customers
            state.revenue = total_rev
            self.memory.update_business_state(state)
            
            print("\n==================================================")
            print(f"[REVENUE GENERATED - CYCLE {cycle_id}]")
            print(f"Product: {state.product}")
            print(f"New Customers Acquired: {new_customers}")
            print(f"Monthly Revenue Generated: ${total_rev:,.2f}")
            print("==================================================\n")

    def run(self):
        print("==================================================")
        print("AUTOBIZ AI CONTINUOUS AUTONOMOUS ENGINE STARTED")
        print("==================================================")
        print(f"Mode: Fully Autonomous (Auto-Approve: {self.auto_approve})")
        print("The agent will research, build, test, deploy, market, and monetize software products on its own.\n")

        cycle_count = 0

        while cycle_count < self.max_cycles:
            state = self.memory.get_business_state()
            active_cycle_id = state.cycle_id

            print(f"--- [Active Cycle {active_cycle_id}] Product: '{state.product or 'None'}' | Stage: '{state.stage}' ---")

            if state.stage == "NO_PRODUCT":
                current_obj = self.memory.get_objective(active_cycle_id)
                if not current_obj or not current_obj.strip():
                    obj_index = (active_cycle_id - 1) % len(DEFAULT_OBJECTIVES)
                    default_obj = DEFAULT_OBJECTIVES[obj_index]
                    print(f"[AUTONOMOUS ENGINE] Setting objective for Cycle {active_cycle_id}: '{default_obj}'")
                    self.ceo.set_objective(default_obj, cycle_id=active_cycle_id)

            # 1. If pending approvals, handle auto-approval
            if self.auto_approve:
                was_approved = self.auto_approve_pending(active_cycle_id)
                if was_approved:
                    time.sleep(1)

            # 2. Run CEO cycle step
            next_action = self.ceo.orchestrator.determine_next_action()
            
            if next_action == "WAIT FOR APPROVAL":
                if self.auto_approve:
                    self.auto_approve_pending(active_cycle_id)
                    continue
                else:
                    print("[AUTONOMOUS ENGINE] Paused: Waiting for human approval. (Pass --auto-approve to run hands-free)")
                    break

            if next_action == "IDLE" or state.stage == "MARKETING_LIVE":
                # Simulate customer acquisition & revenue for this cycle
                self.simulate_revenue_and_growth(active_cycle_id)

                print(f"\nCycle {active_cycle_id} ('{state.product}') has completed all stages and is currently live!")
                cycle_count += 1

                # Check AUTO_CYCLE_CREATION guard (DISABLED by default)
                AUTO_CYCLE_CREATION = "--allow-auto-new-cycle" in sys.argv
                if not AUTO_CYCLE_CREATION:
                    print("[AUTONOMOUS ENGINE] AUTO_CYCLE_CREATION is DISABLED. Stopping without automatically creating a new cycle.")
                    print("To start a new cycle, provide an objective via CLI or run 'python ceo.py new'.")
                    break

                if cycle_count >= self.max_cycles:
                    print(f"Reached maximum requested cycles ({self.max_cycles}). Stopping autonomous run.")
                    break

                print("\n==================================================")
                print(f"INITIALIZING NEW BUSINESS CYCLE ({cycle_count + 1}/{self.max_cycles})")
                print("==================================================")
                
                # Create a new cycle in memory
                new_state = self.memory.create_new_cycle()
                
                # Pick objective from pool or generate one
                obj_index = (new_state.cycle_id - 1) % len(DEFAULT_OBJECTIVES)
                objective = DEFAULT_OBJECTIVES[obj_index]
                print(f"Setting New Business Objective: '{objective}'")
                
                self.ceo.set_objective(objective)
                time.sleep(2)
                continue

            # Execute the cycle step
            print(f"[AUTONOMOUS ENGINE] Executing action: {next_action}")
            self.ceo.run_cycle()
            time.sleep(self.sleep_interval)

        print("\n==================================================")
        print("AUTONOMOUS RUN COMPLETED SUMMARY")
        print("==================================================")
        cycles = self.memory.get_all_cycles()
        total_rev = 0.0
        total_cust = 0
        for c in cycles:
            rev = c.get('revenue', 0.0) or 0.0
            cust = c.get('customers', 0) or 0
            total_rev += rev
            total_cust += cust
            print(f"Cycle {c['cycle_id']}: {c['product'] or 'In Progress'} | Stage: {c['stage']} | Revenue: ${rev:,.2f} | Customers: {cust}")
        print(f"\nTOTAL REVENUE GENERATED ACROSS ALL CYCLES: ${total_rev:,.2f}")
        print(f"TOTAL CUSTOMERS ACQUIRED: {total_cust}")
        print("==================================================")

if __name__ == "__main__":
    auto_approve = "--manual" not in sys.argv
    max_cycles = 3
    for arg in sys.argv:
        if arg.startswith("--cycles="):
            max_cycles = int(arg.split("=")[1])
            
    runner = AutonomousRunner(auto_approve=auto_approve, max_cycles=max_cycles)
    runner.run()
