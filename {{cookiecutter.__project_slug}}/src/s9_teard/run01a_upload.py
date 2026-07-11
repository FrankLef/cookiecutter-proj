# mypy: ignore-errors
"""Upload data to MS Access."""

import duckdb as ddb
from config import settings
from rich.console import Console
from rich.prompt import Confirm

from fltk.prnt.print_msg import print_msg, MsgType

from src._registry.dicz import dicz
from src._registry.acc import main as inst_acc

_sources = dicz.bag("acc").group("upload")


duckdb_path = settings.paths.duckdb
data_path = settings.paths.data


def main(db_choice: str = "main", status_time: str = "5 min") -> None:
    accdb = inst_acc(db_choice=db_choice)
    engin = accdb.engine
    is_ok = Confirm.ask(f"Uploading takes about {status_time}. ok?")
    if not is_ok:
        return
    print_msg("Upload to MS Access.", type=MsgType.PROCESS)
    for table_nm in _sources.keys:
        print_msg(table_nm, type=MsgType.TRACE)
        with ddb.connect(duckdb_path) as conn:
            qry = f"SELECT * FROM {table_nm}"
            data = conn.sql(qry).pl()  # noqa: F841
            console = Console()
            status_msg: str = f"Uploading, {status_time} ..."
            with console.status(status_msg, spinner="bouncingBar"):
                data.write_database(
                    table_name=table_nm, connection=engin, if_table_exists="replace"
                )
