from abc import ABC
from dataclasses import dataclass


@dataclass
class IXbrProperty(ABC):
    name: str


class IXbrProperties(ABC):
    def __init__(self):
        self.props = {}

    def add(self, prop: IXbrProperty) -> None:
        self.props[prop.name] = prop

    def get(self, name: str) -> IXbrProperty:
        prop = self.props[name]
        return prop

    def add_many(self, props: list[IXbrProperty]) -> None:
        for prop in props:
            self.add(prop)

    def get_many(self, names: list[str]) -> list[IXbrProperty]:
        props = []
        for name in names:
            props.append(self.get(name))
        return props
