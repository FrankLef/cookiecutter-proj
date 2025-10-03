import duckdb as ddb


class QryEnums:
    def __init__(self, conn: ddb.DuckDBPyConnection, table_nm: str):
        self._conn = conn
        self._table_nm = table_nm

    @property
    def table_nm(self) -> str:
        return self._table_nm

    def create_enum_by_sum(self, enum_nm: str, col: str, size_col: str) -> None:
        qry = f"DROP TYPE IF EXISTS {enum_nm}"
        self._conn.sql(qry)

        qry = f"""
            CREATE TYPE {enum_nm} AS ENUM
            (
            WITH tmp AS
                (
                SELECT {col}, sum({size_col}) AS tot
                FROM {self._table_nm} GROUP BY {col}
                )
            SELECT {col} FROM tmp ORDER BY tot DESC
            )
            """
        self._conn.sql(qry)

    def apply_enum(self, enum_nm: str, col: str) -> None:
        qry = f"""
        ALTER TABLE {self._table_nm} ALTER COLUMN {col} TYPE {enum_nm};
        """
        self._conn.sql(qry)

    def get_enums(self, enum_nm: str) -> list:
        qry = f"SELECT enum_range(NULL::{enum_nm})"
        enums = self._conn.sql(qry).fetchone()[0]  # type: ignore
        return enums
