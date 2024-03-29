from dataclasses import dataclass

@dataclass
class Port:
    angle: float
    burn_percent: float = 0.0