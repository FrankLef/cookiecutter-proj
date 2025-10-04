import duckdb as ddb
from typing import Iterable


class QryConstraints:
    def __init__(self, conn: ddb.DuckDBPyConnection, table_nm: str):
        self._conn = conn
        self._table_nm = table_nm

    @property
    def table_nm(self) -> str:
        return self._table_nm

    def write_add_primary_key(self, keys: Iterable[str]) -> str:
        the_keys = ",".join(keys)
        qry = f"ALTER TABLE {self._table_nm} ADD PRIMARY KEY ({the_keys})"
        return qry

    def write_set_not_null(self, col: str) -> str:
        qry = f"ALTER TABLE {self._table_nm} ALTER COLUMN {col} SET NOT NULL"
        return qry

    def add_primary_key(self, keys: Iterable[str]) -> None:
        qry = self.write_add_primary_key(keys)
        self._conn.sql(qry)

    def set_not_null(self, cols: Iterable[str]) -> None:
        for col in cols:
            qry = self.write_set_not_null(col)
            self._conn.sql(qry)
