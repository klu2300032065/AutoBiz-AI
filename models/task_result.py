from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class TaskResult:
    status: str
    result: Any
    errors: Optional[str] = None
    artifacts: Optional[str] = None
