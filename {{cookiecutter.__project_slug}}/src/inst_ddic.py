"""Instantiate the TDict and populate it."""

from dataclasses import dataclass
import pandas as pd
from config import settings
from typing import Final

import src.s0_helpers.cls.dic as dic

data_path = settings.paths.data
xbr_xl = settings.ddict.xbr_xl
ref_xl = settings.ddict.ref_xl


@dataclass
class DDicLine(dic.IDicLine):
    pass


class DDicTable(dic.IDicTable):
    def load(self, data: pd.DataFrame):
        for row in data.itertuples():
            line = DDicLine(
                table_nm=row.table_nm,
                name=row.name,
                raw_name=row.raw_name,
                label=row.label,
                raw_dtype=row.raw_dtype,
                dtype=row.dtype,
                activ=row.activ,
                desc=row.desc,
                note=row.note,
            )
            line.read_roles(row.roles)
            self.add(line)


def main(name: str) -> DDicTable:
    SHEET: Final[str] = "data"
    the_sources = {"xbr": xbr_xl, "ref": ref_xl}
    try:
        fn = the_sources[name]
    except KeyError:
        raise KeyError(f"'{name}' is an invalid ddict name.")
    a_file = data_path.joinpath(fn)
    ddic = DDicTable(name=name)
    data = ddic.read_xl(path=a_file, sheet_nm=SHEET)
    ddic.load(data)
    assert len(ddic.lines) != 0, f"The '{name}' ddic has no line."
    return ddic
