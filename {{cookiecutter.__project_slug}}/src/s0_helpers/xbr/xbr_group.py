from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable
import re


@dataclass
class IXbrAttr(ABC):
    name: str
    role: str | None = None
    rule: str | None = None


@dataclass
class IXbrUnit(ABC):
    name: str

    @property
    @abstractmethod
    def attrs(self):
        pass
    
    def get_attrs(self,names:list[str]):
        out=[x for x in self.attrs if x.name in names]
        if not len(out):
            raise AssertionError(f"No attributes available for {names}")
        out = out[0] if len(out) == 1 else out
        return out

    def get_role(self, name: str) -> str | list[str]:
        out = []
        for attr in self.attrs:
            # print("pattern:", rf"\b{name}\b", "role:", attr.role)
            if attr.role:
                a_match = re.search(pattern=rf"\b{name}\b", string=attr.role)
                if a_match is not None:
                    out.append(attr.name)
        if not len(out):
            msg: str = f"No item found for role '{name}'."
            raise KeyError(msg)
        out = out[0] if len(out) == 1 else out
        return out

    def get_rule(self, name: str) -> str | list[str]:
        out = []
        for attr in self.attrs:
            if attr.rule:
                a_match = re.search(pattern=rf"\b{name}\b", string=attr.rule)
                if a_match is not None:
                    out.append(attr.name)
        if not len(out):
            msg: str = f"No item found for rule '{name}'."
            raise KeyError(msg)
        out = out[0] if len(out) == 1 else out
        return out


@dataclass
class IXbrGroup(ABC):
    name: str

    def write_sql(self, vals: Iterable[str]) -> str:
        return ",".join([f"'{x}'" for x in vals])

    def write_csv(self, vals: Iterable[str]) -> str:
        return ",".join(vals)
