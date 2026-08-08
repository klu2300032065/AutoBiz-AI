from memory.business_memory import BusinessMemory
from models.approval import Approval

class ApprovalManager:
    def __init__(self):
        self.memory = BusinessMemory()

    def request_approval(self, action: str, description: str, risk_level: str = "HIGH", estimated_cost: float = 0.0) -> int:
        app = Approval(
            approval_id=0,
            action=action,
            description=description,
            risk_level=risk_level,
            estimated_cost=estimated_cost
        )
        return self.memory.create_approval(app)

    def check_pending_approvals(self) -> bool:
        apps = self.memory.get_pending_approvals()
        return len(apps) > 0

    def approve(self, approval_id: int):
        self.memory.update_approval(approval_id, "APPROVED")

    def reject(self, approval_id: int):
        self.memory.update_approval(approval_id, "REJECTED")
