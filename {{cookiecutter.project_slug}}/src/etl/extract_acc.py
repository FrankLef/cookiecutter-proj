"""Extract data from MS Access."""

from urllib import parse
from pathlib import Path

import pandas as pd
from sqlalchemy import engine, create_engine, exc


def get_engine(
    path: Path,
    mode: str = "Read",
    driver: str = "{Microsoft Access Driver (*.mdb, *.accdb)}",
) -> engine:
    """Create SQLAlchemy engine for MS Access.

    Args:
        path (Path): Path to MS Access database.
        mode (str, optional): Database access mode. Defaults to "Read".
        driver (str, optional): MS Access driver. Don't change this unless you
        know what you are doing. Defaults to "{Microsoft Access Driver (*.mdb, *.accdb)}".

    Raises:
        FileNotFoundError: The MS Access file name is invalid.

    Returns:
        engine: SQLAlchemy engine for MS Access.
    """
    if not path.is_file():
        msg = "\n" + str(path) + "\nis an invalid MS Access DB file name."
        raise FileNotFoundError(msg)
    # NOTE: You must use parse.quote_plus to avoid problem with the password
    # when it contains characters such as '@' which creates an invalid url.
    conn = f"DRIVER={driver};DBQ={path};Mode={mode};"
    url = parse.quote_plus(conn)
    url = rf"access+pyodbc://?odbc_connect={url}"
    acc_engine = create_engine(url)
    return acc_engine


def extract_acc(db_path: Path, tbl: str) -> pd.DataFrame:
    """Extract data from MS Access.

    Args:
        db_path (Path): MS Access db path.
        tbl (str): Name of table to extract.

    Returns:
        pd.Dataframe: Dataframe of extracted data.
    """
    engine = get_engine(db_path)
    sql_str = "select * from " + tbl
    try:
        df = pd.read_sql(sql=sql_str, con=engine)
    except exc.SQLAlchemyError as err:
        # https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy
        # msg = str(err.__dict__["orig"])
        msg = str(err)
        msg = str(type(err)) + "\n" + str(err)
        print(msg)
        raise
    engine.dispose()  # disconnect from the database
    return df
