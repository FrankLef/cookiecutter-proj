# mypy: ignore-errors
"""Export files to reports."""

import shutil
from config import settings

from fltk.prnt.print_msg import print_msg, MsgType

from _registry import specs_mstr

_export = specs_mstr.specs("export")

path_data = settings.DPATHS.data
path_reports = settings.RPATHS.figs


def main(is_skipped: bool = False) -> None:
    if is_skipped:
        raise NotImplementedError(f"Skip the '{__name__}' script.")
    msg: str = f"Exporting {_export.df.height} files to:"
    print_msg(msg, type=MsgType.PROCESS)
    print_msg(str(path_reports), type=MsgType.INFO)
    for row in _export.df.iter_rows(named=True):
        print_msg(row["line"], type=MsgType.TRACE)
        src = path_data.joinpath(row["group"], row["line"])
        if not src.exists():
            msg=f"Source file does not exist:\n{src}"
            raise FileNotFoundError(msg)
        dst = path_reports.joinpath(row["line"])
        if not path_reports.exists():
            msg = f"Destination folder does not exist:\n{path_reports}"
            raise FileNotFoundError(msg)
        shutil.copy2(src=src, dst=dst)


if __name__ == "__main__":
    main()
