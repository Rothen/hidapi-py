from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Battery:
    level_percentage: float
    full: bool
    charging: bool
