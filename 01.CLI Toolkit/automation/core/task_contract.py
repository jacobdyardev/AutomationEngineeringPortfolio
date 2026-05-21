from dataclasses import dataclass, field
from typing import List


@dataclass
class TaskResult:
    success: bool
    message: str = ""
    partial: bool = False
    artifacts: List[str] = field(default_factory=list)