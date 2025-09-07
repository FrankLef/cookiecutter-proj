from pathlib import Path
from typing import Any
from great_tables import GT
import plotly.graph_objects as go


class PrintObj:
    def __init__(self, path:Path):
        self._path=path

    @property
    def path(self):
        return self._path

    def run(self, name:str, obj: Any, is_show: bool | None = False)->None:
        path=self._path
        if is_show is not None:
            if is_show:
                obj.show()
            else:
                fn = name + ".html"
                print(f"Printing file '{fn}'")
                path_fn = path.joinpath(fn)
                if isinstance(obj, go.Figure):
                    obj.write_html(path_fn)
                elif isinstance(obj,GT):
                    obj.write_raw_html(path_fn)
                else:
                    msg=f"Cannot handle object of type '{type(obj)}'"
                    raise TypeError(msg)