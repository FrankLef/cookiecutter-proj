from pathlib import Path
import pandas as pd
import sqlalchemy as sa


class ConnectAcc:
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
            print(f"CONNECTION FAILED:\n{e}")
            return False
        return True

    def load(self, data: pd.DataFrame, tbl: str) -> pd.DataFrame:
        """Load data to MS Access.

        Args:
            data (pd.DataFrame): Data frame to upload.
            tbl (str): Name of table to upload to MS Access.

        Returns:
            pd.Dataframe: Dataframe of uploaded data.
        """
        assert isinstance(data, pd.DataFrame)
        assert len(tbl) != 0
        with self._engine.connect() as conn:
            data.to_sql(name=tbl, con=conn, index=False, if_exists="replace")
        return data

    def read(self, qry: str) -> pd.DataFrame:
        """Read  data from MS Access.

        Args:
            qry (str): SQL query to download from MS Access.

        Returns:
            pd.Dataframe: Dataframe of downloaded data.
        """
        assert len(qry) != 0
        with self._engine.connect() as conn:
            a_qry = sa.text(qry)  # must use text to make it executable
            data = pd.read_sql(sql=a_qry, con=conn)
        return data
    
    def path(self):
        return self._path
