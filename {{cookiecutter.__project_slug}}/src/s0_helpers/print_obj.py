from pathlib import Path
from typing import Any
from enum import StrEnum, auto
from great_tables import GT
import plotly.graph_objects as go


class PrintObj:
    class PType(StrEnum):
        NONE = auto()  # auto() gives lowered-case member name
        SHOW = auto()
        FILE = auto()

    def __init__(self, path: Path):
        self._path = path

    @property
    def path(self):
        return self._path

    def run(self, name: str, obj: Any, ptype: PType | str) -> None:
        if not name:
            raise ValueError("The name is empty.")

        if not obj:
            msg: str = f"Object of type '{type(obj)}' is empty."
            raise ValueError(msg)

        ptype = ptype.lower()
        if ptype not in self.PType:
            raise TypeError(f"'{ptype}' is an invalid PType value.")

        path = self._path

        if ptype != self.PType.NONE:
            if ptype == self.PType.SHOW:
                obj.show()
            elif ptype == self.PType.FILE:
                fn = name + ".html"
                print(f"Printing file '{fn}'")
                path_fn = path.joinpath(fn)
                if isinstance(obj, go.Figure):
                    obj.write_html(path_fn)
                elif isinstance(obj, GT):
                    obj.write_raw_html(path_fn)
                else:
                    msg = f"Cannot handle object of type '{type(obj)}'"
                    raise TypeError(msg)
            else:
                msg = f"The ptype {ptype} is not recognised."
                raise ValueError(msg)
