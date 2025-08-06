from dataclasses import dataclass
from dataclasses_json import dataclass_json
import re


@dataclass(frozen=True)
class Line:
    path: str
    file_nm: str
    table_nm: str
    name: str
    raw_name: str
    label: str
    dtype: str
    activ: bool
    role: str | None = None
    process: str | None = None
    rule: str | None = None
    desc: str | None = None
    note: str | None = None
    period: str | None = None
    top: int = 0
    bottom: int = 0
    left1: int = 0
    right1: int = 0
    left2: int = 0
    right2: int = 0


@dataclass_json
@dataclass
class TDict:
    name: str
    lines: list[Line]

    @property
    def nlines(self) -> int:
        return len(self.lines)

    def get_lines(
        self,
        role: str | None = None,
        process: str | None = None,
        rule: str | None = None,
    ) -> list[Line]:
        out = []
        for line in self.lines:
            is_ok: bool = line.activ
            if role:
                is_matched = (
                    re.search(pattern=rf"\b{role}\b", string=line.role) is not None  # type: ignore
                )
                is_ok = is_ok and is_matched
            if process:
                is_matched = (
                    re.search(pattern=rf"\b{process}\b", string=line.process)  # type: ignore
                    is not None  # type: ignore
                )
                is_ok = is_ok and is_matched
            if rule:
                is_matched = (
                    re.search(pattern=rf"\b{rule}\b", string=line.rule) is not None  # type: ignore
                )
                is_ok = is_ok and is_matched
            if is_ok:
                out.append(line)
        return out
