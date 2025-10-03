from abc import ABC
from dataclasses import dataclass
from typing import Final, Iterable


@dataclass()
class IXbrUnit(ABC):
    name: str
    label: str | None = None
    role: str | None = None
    rule: str | None = None

    def has_role(self, role: str, negate: bool) -> bool:
        has_role = self.has_it(choices=self.role, choice=role, negate=negate)
        return has_role

    def has_rule(self, rule: str, negate: bool) -> bool:
        has_rule = self.has_it(choices=self.rule, choice=rule, negate=negate)
        return has_rule

    def has_it(self, choices: str | None, choice: str, negate: bool) -> bool:
        SEP: Final[str] = ","
        has_it: bool = False
        if choices is not None:
            the_choices: str = choices
            choices_list = the_choices.split(sep=SEP)
            has_it = choice in choices_list
        has_it = not has_it if negate else has_it
        return has_it


@dataclass()
class IXbrGroup(ABC):
    name: str
    units: list[IXbrUnit]

    @property
    def names(self) -> list[str]:
        out = [x.name for x in self.units]
        return out

    @property
    def labels(self) -> dict[str, str | None]:
        out = {x.name: x.label for x in self.units}
        return out

    def get_by_role(self, role: str, negate: bool = False) -> list[str]:
        out = [x.name for x in self.units if x.has_role(role=role, negate=negate)]
        return out

    def get_by_rule(self, rule: str, negate: bool = False) -> list[str]:
        out = [x.name for x in self.units if x.has_rule(rule=rule, negate=negate)]
        return out

    def write_sql(self, vals: Iterable[str]) -> str:
        return ",".join([f"'{x}'" for x in vals])

    def write_csv(self, vals: Iterable[str]) -> str:
        return ",".join(vals)
