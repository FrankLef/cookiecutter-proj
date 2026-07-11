# mypy: ignore-errors
"""Export files to reports."""

import shutil
from config import settings

from fltk.prnt.print_msg import print_msg, MsgType

from src._registry.dicz import dicz

_output = dicz.bag("output")

path_data = settings.paths.data
path_reports = settings.paths.reports_figs


def main(is_skipped: bool = False) -> None:
    if is_skipped:
        raise NotImplementedError(f"Skip the '{__name__}' script.")

    for group_nm, group in _output.coll.items():
        msg: str = f"Exporting {group.nlines} files from {group_nm} to:"
        print_msg(msg, type=MsgType.PROCESS)
        print_msg(str(path_reports), type=MsgType.INFO)
        for line_nm in group.keys:
            print_msg(line_nm, type=MsgType.TRACE)
            src = path_data.joinpath(group_nm, line_nm)
            dest = path_reports.joinpath(line_nm)
            shutil.copy2(src=src, dst=dest)


if __name__ == "__main__":
    main()
