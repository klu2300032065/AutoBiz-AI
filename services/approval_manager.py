from typing import Optional
from memory.business_memory import BusinessMemory
from models.approval import Approval

class ApprovalManager:
    def __init__(self):
        self.memory = BusinessMemory()

    def request_approval(
        self,
        action: str,
        description: str,
        risk_level: str = "HIGH",
        estimated_cost: float = 0.0,
        actual_cost: float = 0.0,
        demo_cost: float = 0.0,
        deployment_mode: str = "LOCAL/DEMO",
        cycle_id: Optional[int] = None
    ) -> int:
        state = self.memory.get_business_state()
        c_id = cycle_id if cycle_id is not None else state.cycle_id
        if deployment_mode == "LOCAL/DEMO":
            actual_cost = 0.0
        app = Approval(
            approval_id=0,
            action=action,
            description=description,
            risk_level=risk_level,
            estimated_cost=estimated_cost,
            actual_cost=actual_cost,
            demo_cost=demo_cost,
            deployment_mode=deployment_mode,
            cycle_id=c_id
        )
        return self.memory.create_approval(app)

    def get_pending_approvals(self, cycle_id: Optional[int] = None) -> list:
        if cycle_id is None:
            state = self.memory.get_business_state()
            cycle_id = state.cycle_id
        return self.memory.get_pending_approvals(cycle_id=cycle_id)

    def check_pending_approvals(self, cycle_id: Optional[int] = None) -> bool:
        if cycle_id is None:
            state = self.memory.get_business_state()
            cycle_id = state.cycle_id
        apps = self.memory.get_pending_approvals(cycle_id=cycle_id)
        return len(apps) > 0

    def approve(self, approval_id: int) -> bool:
        self.memory.update_approval(approval_id, "APPROVED")
        return True

    def reject(self, approval_id: int) -> bool:
        self.memory.update_approval(approval_id, "REJECTED")
        return True
