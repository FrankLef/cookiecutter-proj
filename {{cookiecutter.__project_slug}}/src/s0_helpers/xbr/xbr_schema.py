from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable
import re


@dataclass(frozen=True)
class IXbrAttr(ABC):
    name: str
    role: str | None = None
    rule: str | None = None


@dataclass(frozen=True)
class IXbrTbl(ABC):
    name: str

    @property
    @abstractmethod
    def attrs(self):
        pass

    def get_attrs(self, names: list[str], keep_list: bool = False):
        out = [x for x in self.attrs if x.name in names]
        if not len(out):
            raise KeyError(f"No attributes available for '{names}'.")
        if not keep_list and len(out) == 1:
            out = out[0]
        return out

    def get_role(self, name: str, keep_list: bool = False) -> str | list[str]:
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
        if not keep_list and len(out) == 1:
            out = out[0]
        return out

    def get_rule(self, name: str, keep_list: bool = False) -> str | list[str]:
        out = []
        for attr in self.attrs:
            if attr.rule:
                a_match = re.search(pattern=rf"\b{name}\b", string=attr.rule)
                if a_match is not None:
                    out.append(attr.name)
        if not len(out):
            msg: str = f"No item found for rule '{name}'."
            raise KeyError(msg)
        if not keep_list and len(out) == 1:
            out = out[0]
        return out


@dataclass(frozen=True)
class IXbrSchema(ABC):
    name: str

    def write_sql(self, vals: Iterable[str]) -> str:
        return ",".join([f"'{x}'" for x in vals])

    def write_csv(self, vals: Iterable[str]) -> str:
        return ",".join(vals)
