# mypy: ignore-errors
"""Create MS Access connection."""

from pathlib import Path

from config import settings

from fltk.conn.connect_acc import ConnectAcc


def main(db_choice: str) -> ConnectAcc:
    paths = {
        "main": Path(settings.acc.main),
        "raw": Path(settings.acc.raw),
        "xbr": Path(settings.acc.xbr),
    }
    try:
        path = paths[db_choice]
    except KeyError as e:
        msg: str = f"'{db_choice}' is an invalid MS Access choice."
        e.add_note(msg)
        raise
    conn = ConnectAcc(path=path)
    return conn