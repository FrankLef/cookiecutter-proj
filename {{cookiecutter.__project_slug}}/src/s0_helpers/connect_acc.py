from pathlib import Path
import pandas as pd
import sqlalchemy as sa


class ConnectAcc:
    """Connect to MS Access using SQLAlchemy."""
    def __init__(self, path: Path):
        self._path = path
        self._engine = self._build_engine(path)

    def _build_engine(self, path: Path):
        """Create SQLAlchemy engine for MS Access.

        Args:
            path (Path): Path to MS Access database.

        Raises:
            FileNotFoundError: SQLAlchemy engine for MS Access.

        Returns:
            _type_: The MS Access file name is invalid.
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
        an_engine = sa.create_engine(engine_url)
        return an_engine

    def test_connect(self):
        try:
            with self._engine.connect() as conn:
                conn.execute(sa.text("SELECT 1"))
        except (sa.exc.DBAPIError, sa.exc.OperationalError) as e:
            msg = f"CONNECTION FAILED:\n{e}"
            raise sa.exc.DBAPIError(msg)
        finally:
            self._engine.dispose()
        return True

    def load(self, data: pd.DataFrame, tbl: str) -> pd.DataFrame:
        """Upload data to MS Access.
        
        IMPORTANT: The `con` parameter actually take an SQLAlchemy engine,
        NOT a connection!!  This is different than for `pandas.read_sql` and
        what is usually done.  This is in the description of the `con` argument
        and is EASILY MISSED.  See https://stackoverflow.com/questions/51170169/clean-up-database-connection-with-sqlalchemy-in-pandas for a discussion.

        Args:
            data (pd.DataFrame): Data to upload to MS Access.
            tbl (str): Name of the table in MS Access.

        Returns:
            pd.DataFrame: The original data is returned as is.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("'data' must be a pandas dataframe.")
        if len(tbl) == 0:
            raise ValueError("The table is an empty string.")
        # Important: `con` argument takes en engine, not a connection!
        data.to_sql(name=tbl, con=self._engine, index=False,if_exists='replace')
        self._engine.dispose()
        return data

    def read(self, qry: str) -> pd.DataFrame:
        """Download  data from MS Access.
        
        IMPORTANT: Make sure you use SQLAlchemy `text()` to format the query so
        that it is useable by the engine.

        Args:
            qry (str): SQL query to download from MS Access.

        Returns:
            pd.Dataframe: Dataframe of downloaded data.
        """
        if len(qry) == 0:
            raise ValueError("The query is an empty string.")
        with self._engine.connect() as conn:
            a_qry = sa.text(qry)  # Important: use sa.text().
            data = pd.read_sql(sql=a_qry, con=conn)
        self._engine.dispose()
        return data

    @property
    def path(self) -> Path:
        return self._path
