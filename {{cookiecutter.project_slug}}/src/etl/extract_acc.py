"""Extract data from MS Access."""
import urllib
from pathlib import Path

import pandas as pd
import sqlalchemy as sa


def build_engine(path: Path) -> sa.engine:
    """Create SQLAlchemy engine for MS Access.
    Args:
        path (Path): Path to MS Access database.
    Returns:
        sa.engine: SQLAlchemy engine for MS Access.
    Raises:
        FileNotFoundError: The MS Access file name is invalid.
    """
    if not path.is_file():
        msg = "\n" + str(path) + "\nis an invalid MS Access DB file name."
        raise FileNotFoundError(msg)
    db_driver = "{Microsoft Access Driver (*.mdb, *.accdb)}"
    conn_str = f"DRIVER={db_driver};" f"DBQ={path};" "Mode=Read;"
    url_str = urllib.parse.quote_plus(conn_str)
    url_str = rf"access+pyodbc://?odbc_connect={url_str}"
    acc_engine = sa.create_engine(url_str)
    return acc_engine


def extract_acc(db_path: Path, tbl: str) -> pd.DataFrame:
    """Extract data from MS Access.

    Args:
        db_path (Path): MS Access db path.
        tbl (str): Name of table to extract.

    Returns:
        pd.Dataframe: Dataframe of extracted data.
    """
    engine = build_engine(db_path)
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
    engine.dispose()
    return df
