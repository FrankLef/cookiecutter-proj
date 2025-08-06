"""Xbr objects. Using the the composite design pattern."""

from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import re
from typing import Any


@dataclass
class IXbr(ABC):
    name: str
    label: str | None = None
    roles: set[str] = field(default_factory=set[str])

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Xbr name cannot be empty.")
        self.validate_name(self.name)
        if not self.label:
            self.label = self.name
        if self.roles:
            for role in self.roles:
                self.validate_name(role)

    def validate_name(self, name: str):
        if re.search(pattern=r"\W+", string=name) is not None:
            msg = f"The string '{name}' must have only word characters."
            raise ValueError(msg)
        return name

    def has_roles(
        self, roles_from_user: set[str] = set(), roles_from_container: set[str] = set()
    ) -> bool:
        roles_choices: set[str] = roles_from_container.union(roles_from_user)
        out: bool = roles_choices.issubset(self.roles)
        return out

    @abstractmethod
    def write_sql(self, *args):
        """Get the selected names useable for SQL string."""
        pass


@dataclass
class XbrValue(IXbr):
    def write_sql(self):
        out = f"'{self.name}'"
        return out


@dataclass
class XbrColumn(IXbr):
    dtype: str = "VARCHAR"

    def write_sql(self):
        out = f"{self.name} AS {self.dtype}"
        return out


@dataclass
class XbrContainer(IXbr):
    items: dict[str, IXbr] = field(default_factory=dict[str, IXbr])

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.items, dict):
            raise TypeError("Items must be of type dict[str, IXbr]")

    def write_sql(self, roles: set[str] = set()) -> str:
        """Get the selected names useable for SQL string."""
        the_names = list(self.get_names(roles=roles))
        the_names.sort()
        # the_items = [self.items[x] for x in the_names]
        the_sql = [val.write_sql() for nm, val in self.items.items() if nm in the_names]
        out = ",".join(the_sql)
        return out

    def write_csv(self, roles: set[str] = set()) -> str:
        """Get the selected names as a comma-delimited string."""
        the_names = list(self.get_names(roles=roles))
        the_names.sort()
        out = ",".join(the_names)
        return out

    def add(self, item: IXbr):
        name = self.validate_name(item.name)
        if name in self.items.keys():
            msg = f"'{name}' is already in the item. The old item will be overwritten."
            raise UserWarning(msg)
        self.items[name] = item

    def get_names(self, roles: set[str] = set()) -> list[str]:
        """The set of item names, filtered by role. if roles is empty, it will return all names."""
        if roles:
            for role in roles:
                self.validate_name(role)
        out = [
            nm
            for nm, val in self.items.items()
            if val.has_roles(roles_from_user=roles, roles_from_container=self.roles)
        ]
        if not len(out):
            msg = "No names returned for the roles '{roles}'."
            raise AssertionError(msg)
        return out

    def get_item(self, name: str) -> Any:
        the_items = [x for x in self.items.values() if x.name == name]
        if the_items:
            if len(the_items) == 1:
                out = the_items[0]
            else:
                msg = f"""
                The name '{name}' returned {len(the_items)} items.
                There must be only 1. This is really weird.
                """
                raise KeyError(msg)
        else:
            msg = f"The name '{name}' returned no item."
            raise KeyError(msg)
        return out

    def get_items(self, roles: set[str] = set()) -> list[Any]:
        """Get a set of items from the container, filtered by role."""
        the_names = self.get_names(roles=roles)
        assert len(the_names) != 0, "No names were found by get_items()."
        out = [x for x in self.items.values() if x.name in the_names]  # type: ignore
        return out
