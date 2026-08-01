"""Create the duckdb connection used by the projet."""

import duckdb
from config import settings

type DdbConn = duckdb.DuckDBPyConnection

duckdb_path = settings.paths.duckdb


def get_conn() -> DdbConn:
    """Create duckdb connection.

    Returns:
        DdbConn: Duckdb connection for Python.
    """
    return duckdb.connect(duckdb_path)
