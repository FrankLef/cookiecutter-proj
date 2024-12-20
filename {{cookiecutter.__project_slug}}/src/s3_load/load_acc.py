"""Load/Extract data to/from MS Access."""

from pathlib import Path

import pandas as pd
import sqlalchemy as sa


def build_engine(path: Path):
    """Create SQLAlchemy engine for MS Access.

    Args:
        path (Path): Path to MS Access database.

    Returns:
        sa.engine: SQLAlchemy engine for MS Access.

    Raises:
        FileNotFoundError: The MS Access file name is invalid.
    """
    if not path.is_file():
        msg = "\n" + str(path) + "\nis an invalid MS Access file name."
        raise FileNotFoundError(msg)
    db_driver = "{Microsoft Access Driver (*.mdb, *.accdb)}"
    conn_str = f"DRIVER={db_driver};DBQ={path};"
    # print(f"{conn_str=}")
    engine_url = sa.engine.url.URL.create(
        drivername="access+pyodbc", query={"odbc_connect": conn_str}
    )
    acc_engine = sa.create_engine(engine_url)
    # Test the connection
    try:
        with acc_engine.connect() as conn:
            conn.execute(sa.text("SELECT 1"))
    except (sa.exc.DBAPIError, sa.exc.OperationalError) as e:
        print(f"CONNECTION FAILED:\n{e}")
    return acc_engine


def load_acc(data: pd.DataFrame, in_path: Path, db_path: Path, tbl: str) -> pd.DataFrame:
    """Load data to MS Access.

    Args:
        in_path (Path): Full name of excel file to upload.
        db_path (Path): MS Access db path.
        tbl (str): Name of table to upload to MS Access.

    Returns:
        pd.Dataframe: Dataframe of uploaded data.
    """
    acc_engine = build_engine(db_path)
    with acc_engine.connect() as conn:
        data.to_sql(name=tbl, con=conn, index=False, if_exists="replace")
    acc_engine.dispose()
    return data


def read_acc(out_path: Path, db_path: Path, qry: str) -> pd.DataFrame:
    """Read  data from MS Access.

    Args:
        out_path (Path): Full name of excel file to save.
        db_path (Path): MS Access db path.
        qry (str): SQL query to download from MS Access.

    Returns:
        pd.Dataframe: Dataframe of downloaded data.
    """
    acc_engine = build_engine(db_path)
    with acc_engine.connect() as conn:
        data = pd.read_sql(sql=qry, con=conn)
    acc_engine.dispose()
    return data
