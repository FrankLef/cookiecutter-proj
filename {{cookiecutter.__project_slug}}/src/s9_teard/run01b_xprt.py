# mypy: ignore-errors
"""Export files to reports."""

import shutil
from config import settings

from fltk.prnt.print_msg import print_msg, MsgType

from src._registry.specs import specs_mstr

_output = specs_mstr.specs("output")

path_data = settings.paths.data
path_reports = settings.paths.reports_figs


def main(is_skipped: bool = False) -> None:
    if is_skipped:
        raise NotImplementedError(f"Skip the '{__name__}' script.")
    msg: str = f"Exporting {_output.df.height} files to:"
    print_msg(msg, type=MsgType.PROCESS)
    print_msg(str(path_reports), type=MsgType.INFO)
    for row in _output.df.iter_rows(named=True):
        print_msg(row["line"], type=MsgType.TRACE)
        src = path_data.joinpath(row["group"], row["line"])
        dst = path_reports.joinpath(row["line"])
        shutil.copy2(src=src, dst=dst)


if __name__ == "__main__":
    main()
