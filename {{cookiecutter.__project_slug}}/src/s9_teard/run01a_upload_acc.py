# mypy: ignore-errors
"""Upload data to MS Access."""

from config import settings
import polars as pl
from sqlalchemy import types
from typing import Any
from datetime import datetime as dt
from rich.console import Console
from rich.prompt import Confirm

from fltk.prnt.print_msg import print_msg, MsgType

from src._registry.dicz import dicz
from src._registry.ddb import get_conn
from src._registry.acc import main as inst_acc

_sources = dicz.bag("acc").group("upload")


data_path = settings.paths.data


def cast_shortstr(data: pl.DataFrame) -> pl.DataFrame:
    """Cast to short string to avoind memo ftype (long text) in MS Access."""
    data = data.with_columns(pl.col(pl.String).str.slice(0, 255))
    return data


def get_dtype_mapping(data: pl.DataFrame) -> dict[str, Any]:
    """Create dtype mapping with SQL Alchemy to have short text in MS Access."""
    string_cols = [
        col for col, dtype in zip(data.columns, data.dtypes) if dtype == pl.String
    ]
    dtype_mapping = {col: types.VARCHAR(255) for col in string_cols}
    return dtype_mapping


def main(db_choice: str = "main", wait_time: str = "5 min") -> None:
    accdb = inst_acc(db_choice=db_choice)
    engin = accdb.engine
    is_ok = Confirm.ask(f"Uploading takes about {wait_time}. ok?")
    if not is_ok:
        return
    start_time: str = dt.now().strftime("%H:%M:%S")
    print_msg(f"Start time: {start_time}", type=MsgType.INFO)
    print_msg("Upload to MS Access.", type=MsgType.PROCESS)
    for table_nm in _sources.keys:
        print_msg(table_nm, type=MsgType.TRACE)
        with get_conn() as conn:
            data = conn.sql(f"FROM {table_nm};").pl()
            data = cast_shortstr(data)
            dtype_mapping = get_dtype_mapping(data)
            console = Console()
            status_msg: str = f"Uploading, {wait_time} ..."
            with console.status(status_msg, spinner="bouncingBar"):
                data.write_database(
                    table_name=table_nm,
                    connection=engin,
                    if_table_exists="replace",
                    engine_options={"dtype": dtype_mapping},
                )
    end_time: str = dt.now().strftime("%H:%M:%S")
    print_msg(f"End time: {end_time}", type=MsgType.INFO)
