from abc import ABC
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class IXbrTbl(ABC):
    name: str


@dataclass(frozen=True)
class IXbrSchema(ABC):
    name: str

    def write_sql(self, vals: Iterable[str]) -> str:
        return ",".join([f"'{x}'" for x in vals])

    def write_csv(self, vals: Iterable[str]) -> str:
        return ",".join(vals)
