"""TDict and DDict classes."""

from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import re
# from typing import Any


@dataclass
class IDicLine(ABC):
    name: str
    raw_name: str | None = None
    label: str | None = None
    raw_dtype: str | None = None
    dtype: str | None = None
    activ: bool = True
    desc: str | None = None
    note: str | None = None
    roles: set[str] = field(default_factory=lambda: set())

    def has_roles(self, roles: set[str] = set()) -> bool:
        return roles.issubset(self.roles)

    def read_roles(self, roles: str) -> None:
        the_roles = re.split(pattern=r"\W", string=roles)
        out = set(the_roles) if len(the_roles) else set()
        self.roles = out


@dataclass
class IDicTable(ABC):
    name: str
    lines: list[IDicLine] = field(default_factory=lambda: list())

    def get_activ_lines(self) -> tuple[IDicLine, ...]:
        out = tuple([x for x in self.lines if x.activ])
        return out

    def add(self, line):
        self.lines.append(line)

    @abstractmethod
    def load(self, *args):
        pass


@dataclass
class TDicLine(IDicLine):
    path: str | None = None
    file_nm: str | None = None
    table_nm: str | None = None
