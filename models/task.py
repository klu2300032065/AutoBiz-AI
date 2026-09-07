from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Task:
    task_id: int
    type: str
    description: str
    status: str = "PENDING"
    priority: int = 1
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    dependencies: List[int] = field(default_factory=list)
    assigned_agent: Optional[str] = None
    input_data: Optional[str] = None
    result: Optional[str] = None
    cycle_id: int = 1
