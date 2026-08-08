from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BusinessState:
    product: Optional[str] = None
    stage: str = "RESEARCH"
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
