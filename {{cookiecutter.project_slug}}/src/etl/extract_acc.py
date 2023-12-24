"""Extract data from MS Access."""
import urllib
from pathlib import Path

import pandas as pd
import sqlalchemy as sa
from prefect import task


def build_engine(path: str) -> sa.engine:
    """Create SQLAlchemy engine for MS Access.
    Args:
        path (str): Path to MS Access database.
    Returns:
        sa.engine: SQLAlchemy engine for MS Access.
    Raises:
        FileNotFoundError: The MS Access file name is invalid.
    """
    if Path(path).is_file() is False:
        msg = "\n" + path + "\nis an invalid MS Access DB file name."
        raise FileNotFoundError(msg)
    db_driver = "{Microsoft Access Driver (*.mdb, *.accdb)}"
    conn_str = f"DRIVER={db_driver};" f"DBQ={path};" "Mode=Read;"
    url_str = urllib.parse.quote_plus(conn_str)
    url_str = rf"access+pyodbc://?odbc_connect={url_str}"
    acc_engine = sa.create_engine(url_str)
    return acc_engine


def extract_data(tables: tuple[str, ...], engine: sa.engine) -> dict:
    """Extract data from MS Access.
    Args:
        tables (set[str]): Names of tables.
        engine (sa.engine): SQLAlchemy engine for MS Access.
    Returns:
        dict: Datasets from MS Access.
    """

    out = {}
    for tbl in tables:
        sql_str = "select * from " + tbl
        try:
            df = pd.read_sql(sql=sql_str, con=engine)
        except sa.SQLAlchemyError as err:
            # https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy
            # msg = str(err.__dict__["orig"])
            msg = str(err)
            msg = "THE ERROR:" + str(type(err))
            print(msg)
            raise
        out[tbl] = df
    engine.dispose()
    return out


@task
def extract_acc(path: str, tables: tuple[str, ...]) -> dict:
    acc_engine = build_engine(path=path)
    data = extract_data(tables=tables, engine=acc_engine)
    # print the shape of every table
    # {tbl: print(df.shape) for (tbl, df) in raw_data.items()}
    return data
