"""TDict and DDict classes."""

from dataclasses import dataclass
from abc import ABC, abstractmethod
import duckdb as ddb
import re
from pathlib import Path
import pandas as pd
from typing import Final


@dataclass
class IDicLine(ABC):
    table_nm: str
    name: str
    raw_name: str
    label: str
    raw_dtype: str
    dtype: str
    activ: bool
    rules: str
    roles: str
    desc: str
    note: str

    @staticmethod
    def check_txt(txt: str | None, target: str | None) -> bool:
        out: bool = True
        if txt:
            if target is not None:
                txt = txt.strip()
                pat: str = rf"\b{txt}\b"
                out = re.search(pattern=pat, string=target) is not None
            else:
                out = False
        return out

    def is_select(
        self,
        table_nm: str | None = None,
        rule: str | None = None,
        role: str | None = None,
    ) -> bool:
        out: bool = (
            self.check_txt(txt=table_nm, target=self.table_nm)
            and self.check_txt(txt=rule, target=self.rules)
        ) and self.check_txt(txt=role, target=self.roles)
        return out


class IDicTable(ABC):
    def __init__(self, name: str):
        self._name = name
        self._lines: list[IDicLine] = []

    @property
    def name(self):
        return self._name

    @property
    def lines(self):
        return self._lines

    def write_csv(
        self,
        table_nm: str | None,
        rule: str | None = None,
        role: str | None = None,
        is_activ_only: bool = True,
    ) -> str:
        """Get the selected names as a comma-delimited string."""
        the_lines = self.get_lines(
            table_nm=table_nm, rule=rule, role=role, is_activ_only=is_activ_only
        )
        the_names = [x.name for x in the_lines]
        out: str = ",".join(the_names)
        return out

    def get_lines(
        self,
        table_nm: str | None,
        rule: str | None = None,
        role: str | None = None,
        is_activ_only: bool = True,
    ) -> list[IDicLine]:
        the_lines = [
            x
            for x in self.lines
            if x.is_select(table_nm=table_nm, rule=rule, role=role)
        ]
        if is_activ_only:
            the_lines = [x for x in the_lines if x.activ]
        return the_lines

    def read_xl(self, path: Path, sheet_nm: str) -> pd.DataFrame:
        """Read an excel file containing the data to load into dic."""
        # NOTE: Important to specify the dtypes for excel.
        # Otherwise problem, e.g. with the activ field which will not be interpreted as boolean
        xl_dtypes = {
            "activ": bool,
            "rules": str,
            "roles": str,
            "desc": str,
            "note": str,
        }
        data = pd.read_excel(io=path, sheet_name=sheet_nm, dtype=xl_dtypes)
        msg = f"The excel data for dic '{self.name}' is empty."
        assert not data.empty, msg
        EMPTY_STR: Final[str] = ""
        VARS: Final[tuple[str, ...]] = ("rules", "roles", "desc", "note")
        # NOTE: Remove NaN put by pandas. Not sure this is necessary anymore since using xl_dtypes above.  Keep it.
        for var in VARS:
            data[var] = data[var].fillna(EMPTY_STR)
        return data

    def set_pk(
        self, conn: ddb.DuckDBPyConnection, table_nm: str, rule: str = "pk"
    ) -> None:
        """Set the primary key of a table."""
        pk_csv: str = self.write_csv(table_nm=table_nm, rule=rule)
        if not len(pk_csv):
            raise ValueError(f"No PRIMARY KEY lines with rule '{rule}'")
        qry = f"ALTER TABLE {table_nm} ADD PRIMARY KEY ({pk_csv})"
        conn.sql(qry)

    def set_nn(
        self, conn: ddb.DuckDBPyConnection, table_nm: str, rule: str = "nn"
    ) -> None:
        """Set columns to NOT NULL."""
        the_lines = self.get_lines(table_nm=table_nm, rule=rule)
        if not len(the_lines):
            raise ValueError(f"No NOT NULL lines with rule '{rule}'")
        for line in the_lines:
            qry = f"""
            ALTER TABLE {table_nm} ALTER COLUMN {line.name}
            SET NOT NULL
            """
            conn.sql(qry)

    def ren_col(
        self, conn: ddb.DuckDBPyConnection, table_nm: str, rule: str = "ren"
    ) -> None:
        """Rename columns."""
        the_lines = self.get_lines(table_nm=table_nm, rule=rule)
        if not len(the_lines):
            raise ValueError(f"No RENAME lines with rule '{rule}'")
        for line in the_lines:
            # NOTE: Parser exception might be caused by using a reserved word. Use double quotes to prevent this.
            qry = f'''
            ALTER TABLE {table_nm}
            RENAME COLUMN "{line.raw_name}" TO {line.name}
            '''
            conn.sql(qry)

    def add(self, line):
        self.lines.append(line)

    @abstractmethod
    def load(self, *args):
        pass


@dataclass
class TDicLine(IDicLine):
    path: str | None = None
    file_nm: str | None = None
