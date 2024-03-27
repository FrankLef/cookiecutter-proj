"""Extract data from MS Access."""

from urllib import parse
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, exc
from sqlalchemy.engine.base import Engine  # for type hint

specs: dict[str, str] = {
    "path": r"C:/Users/Public/MyJob/DesjCap_cies/NSE/OlapNse_V02/db_NSE_V02.accdb",
    "mode": 'Read',
    "driver": '{Microsoft Access Driver (*.mdb, *.accdb)}'
}


def get_engine(
    path: str = specs['path'],
    mode: str = specs['mode'],
    driver: str = specs['driver'],
) -> Engine:
    """Create SQLAlchemy engine for MS Access.

    Args:
        path (str, optional): Path to MS Access db. Defaults to specs['path'].
        mode (str, optional): Mode. Defaults to specs['mode'].
        driver (str, optional): Driver name. Defaults to specs['driver'].

    Raises:
        FileNotFoundError: The database was not found.

    Returns:
        Engine: Engine to access MS Access.
    """
    path = Path(path)  # type:ignore
    if not path.is_file():  # type: ignore
        msg = "\n" + str(path) + "\nis an invalid MS Access DB file name."
        raise FileNotFoundError(msg)
    # NOTE: You must use parse.quote_plus to avoid problem with the password
    # when it contains characters such as '@' which creates an invalid url.
    conn = f"DRIVER={driver};DBQ={path};Mode={mode};"
    url = parse.quote_plus(conn)
    url = rf"access+pyodbc://?odbc_connect={url}"
    engine = create_engine(url)
    return engine


def extract_acc(sql: str) -> pd.DataFrame:
    """Extract data from MS Access.

    Args:
        sql (str): Query used to get data.

    Returns:
        pd.DataFrame: Data rturned from MS Access.
    """
    engine = get_engine()
    try:
        df = pd.read_sql(sql=sql, con=engine)
    except exc.SQLAlchemyError as err:
        # https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy
        # msg = str(err.__dict__["orig"])
        msg = str(err)
        msg = str(type(err)) + "\n" + str(err)
        print(msg)
        raise
    engine.dispose()  # disconnect from the database
    return df


if __name__ == "__main__":
    engine = get_engine()
    print(engine.url)