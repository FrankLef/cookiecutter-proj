"""Create the duckdb connection used by the projet."""

from pathlib import Path
import duckdb

type DdbConn = duckdb.DuckDBPyConnection

# NOTE: need the ddb_path in settings because used by ddb_compact
DDB_PATH = Path(__file__).parents[1].joinpath("data", "todo.duckdb")


def ddb_conn() -> DdbConn:
    """Create duckdb connection.

    Returns:
        DdbConn: Duckdb connection for Python.
    """
    conn = duckdb.connect(DDB_PATH)
    return conn


DDB_CONN = ddb_conn
