from dataclasses import dataclass, field


@dataclass
class DiscoveryResult:
    tasks: dict = field(default_factory=dict)
    failed: dict = field(default_factory=dict)