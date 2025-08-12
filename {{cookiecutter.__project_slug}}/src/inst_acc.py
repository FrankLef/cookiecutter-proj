"""Instantiate a connection to a MS Access database."""

from pathlib import Path
from typing import Any

from config import settings

from src.s0_helpers import connect_acc


def main(db_choice: str) -> tuple[Any, Path]:
    match db_choice:
        case "db":
            path = Path(settings.acc_db.fn)
        case "raw":
            path = Path(settings.acc_raw_db.fn)
        case _:
            msg: str = f"'{db_choice}' is an invalid db choice for accdb_conn."
            raise ValueError(msg)
    conn = connect_acc.ConnectAcc(path=path)
    return (conn, path)
