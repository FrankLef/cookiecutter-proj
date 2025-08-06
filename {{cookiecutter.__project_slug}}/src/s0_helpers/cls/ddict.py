from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass(frozen=True)
class Line:
    name: str
    raw_name: str
    label: str
    raw_dtype: str
    dtype: str
    activ: bool
    is_pk: bool
    null_ok: bool
    role: str | None = None
    process: str | None = None
    rule: str | None = None
    desc: str | None = None
    note: str | None = None


@dataclass
class Table:
    name: str
    lines: list[Line]

    def get_columns(self) -> list[str]:
        lines = self.lines
        vars = {line.name: [line.dtype, line.null_ok] for line in lines}
        out = []
        for col, val in vars.items():
            dtype = val[0]
            is_null_ok = val[1]
            if is_null_ok:
                out.append(f"{col} {dtype}")
            else:
                out.append(f"{col} {dtype} NOT NULL")
        return out

    def get_pk(self) -> list[str]:
        lines = self.lines
        out = [line.name for line in lines if line.is_pk]
        return out


@dataclass_json
@dataclass
class DDict:
    name: str
    tables: list[Table]

    @property
    def nlines(self) -> int:
        nb = [len(tbl.lines) for tbl in self.tables]
        n: int = sum(nb)
        return n
