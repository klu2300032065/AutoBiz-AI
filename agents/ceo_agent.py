from agents.orchestrator import Orchestrator
from services.agent_registry import AgentRegistry
from services.task_manager import TaskManager
from memory.business_memory import BusinessMemory
import json
import re

class CEOAgent:
    def __init__(self):
        self.orchestrator = Orchestrator()
        self.registry = AgentRegistry()
        self.task_manager = TaskManager()
        self.memory = BusinessMemory()

    def set_objective(self, objective: str):
        self.memory.set_objective(objective)

    def run_cycle(self):
        print("CEO: Analyzing business state...")
        next_action = self.orchestrator.determine_next_action()
        print(f"CEO: Next action determined: {next_action}")
        
        if next_action == "WAIT FOR APPROVAL":
            print("CEO: Halting execution. Human approval required.")
            return

        if next_action == "IDLE":
            print("CEO: No pending actions. Everything is running smoothly.")
            return

        state = self.memory.get_business_state()
        task = self.task_manager.get_next_runnable_task(cycle_id=state.cycle_id)
        if not task:
            return
            
        print(f"CEO: Executing task {task.task_id}: {task.type}")
        self.task_manager.update_task_status(task.task_id, "RUNNING", assigned_agent=task.type)
        
        # Prepare input data for the agent
        state = self.memory.get_business_state()
        input_data = None
        
        if task.type == "RESEARCH_PRODUCT":
            input_data = self.memory.get_objective(state.cycle_id)
            if not input_data or not input_data.strip():
                input_data = "Find software products that Indian college students would realistically pay for."
                self.memory.set_objective(input_data, cycle_id=state.cycle_id)
        elif task.type in ["BUILD_PRODUCT", "RUN_QA", "PREPARE_DEPLOYMENT", "CREATE_MARKETING", "ANALYZE_PERFORMANCE"]:
            if task.type == "BUILD_PRODUCT" and state.product is None and state.research_results:
                # Extract product name from research
                match = re.search(r"Product:\s*(.+)", state.research_results)
                if match:
                    state.product = match.group(1).strip()
                    self.memory.update_business_state(state)
                input_data = state.research_results
            else:
                input_data = state.product
                
        task.input_data = input_data
                
        # Execute task (with up to 3 retries)
        retries = 0
        success = False
        result = None
        while retries < 3 and not success:
            res = self.registry.execute_task(task)
            if res.get("status") == "success":
                success = True
                result = res.get("result")
            else:
                retries += 1
                print(f"CEO: Agent failed. Retrying ({retries}/3)... Error: {res.get('errors')}")
                
        if success:
            print(f"CEO: Task {task.task_id} completed successfully.")
            self.task_manager.update_task_status(task.task_id, "COMPLETED", result=str(result))
            
            # Update business state based on task
            state = self.memory.get_business_state()
            if task.type == "RESEARCH_PRODUCT":
                state.research_results = str(result)
                state.stage = "RESEARCH_COMPLETED"
                match = re.search(r"Product:\s*(.+)", str(result))
                if match:
                    p_name = match.group(1).strip()
                    if p_name and not p_name.startswith("Based on"):
                        state.product = p_name
            elif task.type == "BUILD_PRODUCT":
                state.build_status = "COMPLETED"
                state.qa = None
                state.stage = "BUILD_COMPLETED"
            elif task.type == "RUN_QA":
                state.qa = "PASS"
                state.stage = "QA_COMPLETED"
            elif task.type == "PREPARE_DEPLOYMENT":
                state.deployment = "READY"
                state.stage = "DEPLOYMENT_READY"
            elif task.type == "CREATE_MARKETING":
                state.marketing = "READY"
                state.stage = "MARKETING_READY"
                
            self.memory.update_business_state(state)
        else:
            print(f"CEO: Task {task.task_id} FAILED after 3 retries.")
            self.task_manager.update_task_status(task.task_id, "FAILED", result="Failed after 3 retries.")
            
            state = self.memory.get_business_state()
            if task.type == "BUILD_PRODUCT":
                state.build_status = "FAIL"
            elif task.type == "RUN_QA":
                state.qa = "FAIL"
            elif task.type == "PREPARE_DEPLOYMENT":
                state.deployment = "FAIL"
            elif task.type == "CREATE_MARKETING":
                state.marketing = "FAIL"
            self.memory.update_business_state(state)
