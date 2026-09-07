from services.task_manager import TaskManager
from services.approval_manager import ApprovalManager
from memory.business_memory import BusinessMemory
from models.business_state import BusinessState

class Orchestrator:
    def __init__(self):
        self.task_manager = TaskManager()
        self.approval_manager = ApprovalManager()
        self.memory = BusinessMemory()

    def determine_next_action(self):
        state = self.memory.get_business_state()
        pending_apps = self.approval_manager.check_pending_approvals(cycle_id=state.cycle_id)

        if pending_apps:
            return "WAIT FOR APPROVAL"

        # Check existing pending tasks for this active cycle
        next_task = self.task_manager.get_next_runnable_task(cycle_id=state.cycle_id)
        if next_task:
            return next_task.type

        if state.stage == "NO_PRODUCT" or (state.product is None and state.research_results is None):
            # Need to research
            self.task_manager.create_task("RESEARCH_PRODUCT", "Research a new product opportunity", cycle_id=state.cycle_id)
            return "RESEARCH_PRODUCT"
            
        if state.research_results is not None and state.stage == "RESEARCH_COMPLETED":
            # Research done, request human approval for product idea
            import re
            match = re.search(r"Product:\s*(.+)", state.research_results)
            prod_name = match.group(1).strip() if match else "Researched Product Idea"
            self.approval_manager.request_approval(
                "APPROVE_PRODUCT",
                f"Approve the researched product idea '{prod_name}' for building.",
                risk_level="MEDIUM",
                estimated_cost=0.0
            )
            state.stage = "WAITING_PRODUCT_APPROVAL"
            self.memory.update_business_state(state)
            return "WAIT FOR APPROVAL"

        if state.stage == "WAITING_PRODUCT_APPROVAL":
            # If no pending apps and we are in WAITING state, it means it was approved!
            state.stage = "PRODUCT_APPROVED"
            self.memory.update_business_state(state)

        if state.stage == "PRODUCT_APPROVED" and state.build_status is None:
            # Build product
            self.task_manager.create_task("BUILD_PRODUCT", f"Build the product: {state.product}", cycle_id=state.cycle_id)
            return "BUILD_PRODUCT"

        if state.stage == "QA_FAILED_FINAL":
            return "WAIT FOR APPROVAL"

        if state.build_status == "COMPLETED" and state.qa is None:
            # Run QA
            self.task_manager.create_task("RUN_QA", f"Run QA on {state.product}", cycle_id=state.cycle_id)
            return "RUN_QA"

        if state.qa == "FAIL":
            retries = getattr(state, "qa_retry_count", 0)
            if retries >= 3:
                print(f"[ORCHESTRATOR] Max QA retries (3) reached for Cycle {state.cycle_id}. Stage set to QA_FAILED_FINAL. Halting for human approval.")
                state.stage = "QA_FAILED_FINAL"
                self.memory.update_business_state(state)
                return "WAIT FOR APPROVAL"
            else:
                state.qa_retry_count = retries + 1
                state.qa = None
                state.build_status = None
                self.memory.update_business_state(state)
                self.task_manager.create_task("BUILD_PRODUCT", f"Fix QA issues for {state.product} (Attempt {state.qa_retry_count}/3)", cycle_id=state.cycle_id)
                return "BUILD_PRODUCT"

        if state.stage == "QA_COMPLETED" and state.deployment in [None, "FAIL"]:
            # Prepare deployment
            state.deployment = None
            self.memory.update_business_state(state)
            self.task_manager.create_task("PREPARE_DEPLOYMENT", f"Prepare deployment for {state.product}", cycle_id=state.cycle_id)
            return "PREPARE_DEPLOYMENT"

        if state.deployment == "READY" and state.stage == "DEPLOYMENT_READY":
            # Deployment ready, need approval
            self.approval_manager.request_approval(
                "DEPLOY_PRODUCT",
                "Approve deployment to production.",
                risk_level="HIGH",
                estimated_cost=50.0,
                actual_cost=0.0,
                demo_cost=50.0,
                deployment_mode="LOCAL/DEMO"
            )
            # Advance state to prevent looping on this approval condition
            state.stage = "WAITING_DEPLOYMENT_APPROVAL"
            self.memory.update_business_state(state)
            return "WAIT FOR APPROVAL"
            
        if state.stage == "WAITING_DEPLOYMENT_APPROVAL":
            state.stage = "DEPLOYMENT_APPROVED"
            state.deployment = "LIVE"
            self.memory.update_business_state(state)

        if state.stage == "DEPLOYMENT_APPROVED" and state.marketing is None:
            # Run Marketing
            self.task_manager.create_task("CREATE_MARKETING", f"Create marketing for {state.product}", cycle_id=state.cycle_id)
            return "CREATE_MARKETING"
            
        if state.marketing == "READY" and state.stage == "MARKETING_READY":
            # Need approval for marketing
            self.approval_manager.request_approval(
                "LAUNCH_MARKETING",
                "Approve launch of marketing campaigns.",
                risk_level="HIGH",
                estimated_cost=350.0
            )
            state.stage = "WAITING_MARKETING_APPROVAL"
            self.memory.update_business_state(state)
            return "WAIT FOR APPROVAL"
            
        if state.stage == "WAITING_MARKETING_APPROVAL":
            state.stage = "MARKETING_LIVE"
            state.marketing = "LIVE"
            self.memory.update_business_state(state)

        return "IDLE"
