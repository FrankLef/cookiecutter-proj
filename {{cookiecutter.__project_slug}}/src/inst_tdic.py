"""Instantiate the TDict and populate it."""

from dataclasses import dataclass
import pandas as pd
from config import settings
from typing import Final
# from pathlib import Path
# import json

# import src.s0_helpers.richtools as rt
import src.s0_helpers.cls.dic as dic

data_path = settings.paths.data
tdict_xl = settings.tdict.tdict_xl


@dataclass
class TDicLine(dic.IDicLine):
    path: str | None = None
    file_nm: str | None = None
    period: str | None = None
    top: int = 0
    bottom: int = 0
    left1: int = 0
    right1: int = 0
    left2: int = 0
    right2: int = 0


class TDicTable(dic.IDicTable):
    def load(self, data: pd.DataFrame):
        for row in data.itertuples():
            line = TDicLine(
                table_nm=row.table_nm,
                name=row.name,
                raw_name=row.raw_name,
                label=row.label,
                raw_dtype=row.raw_dtype,
                dtype=row.dtype,
                activ=row.activ,
                desc=row.desc,
                note=row.note,
                path=row.path,
                file_nm=row.file_nm,
                period=row.period,
                top=row.top,
                bottom=row.bottom,
                left1=row.left1,
                right1=row.right1,
                left2=row.left2,
                right2=row.right2,
            )
            line.read_roles(row.roles)
            self.add(line)


def main(name: str) -> TDicTable:
    SHEET: Final[str] = "data"
    the_sources = {"main": tdict_xl}
    try:
        fn = the_sources[name]
    except KeyError:
        raise KeyError(f"'{name}' is an invalid tdict name.")
    a_file = data_path.joinpath(fn)
    tdic = TDicTable(name=name)
    data = tdic.read_xl(path=a_file, sheet_nm=SHEET)
    tdic.load(data)
    assert len(tdic.lines) != 0, f"The '{name}' tdic has no line."
    return tdic
