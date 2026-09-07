from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Approval:
    approval_id: int
    action: str
    description: str
    risk_level: str
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    demo_cost: float = 0.0
    deployment_mode: str = "LOCAL/DEMO"
    status: str = "PENDING"
    requested_at: str = field(default_factory=lambda: datetime.now().isoformat())
    cycle_id: Optional[int] = 1

