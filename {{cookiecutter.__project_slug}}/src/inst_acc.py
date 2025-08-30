"""Instantiate a connection to a MS Access database."""

from pathlib import Path

from config import settings

from src.s0_helpers import connect_acc as acc


def main(db_choice: str) -> tuple[acc.ConnectAcc, Path]:
    match db_choice:
        case "db":
            path = Path(settings.db.xbr)
        case "raw":
            path = Path(settings.raw_db.xbr)
        case _:
            msg: str = f"'{db_choice}' is an invalid db choice for accdb_conn."
            raise ValueError(msg)
    conn = acc.ConnectAcc(path=path)
    return (conn, path)
