from abc import ABC
from dataclasses import dataclass


@dataclass
class IBaseGeom(ABC):
    color: str | None = None
    size: float | None = None
    shape: str | None = None


@dataclass
class IBaseFmt(ABC):
    scale: float = 1
    decimals: int = 2
    mask: str = "{:,.2f}"
