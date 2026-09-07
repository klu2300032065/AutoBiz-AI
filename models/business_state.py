from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BusinessState:
    cycle_id: int = 1
    product: Optional[str] = None
    stage: str = "NO_PRODUCT"
    qa: Optional[str] = None
    deployment: Optional[str] = None
    marketing: Optional[str] = None
    revenue: float = 0.0
    customers: int = 0
    next_action: Optional[str] = None
    current_problems: Optional[str] = None
    analytics: Optional[str] = None
    build_status: Optional[str] = None
    research_results: Optional[str] = None
    qa_retry_count: int = 0
