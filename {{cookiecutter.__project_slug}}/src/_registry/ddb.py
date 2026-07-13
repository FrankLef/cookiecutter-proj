"""Create Duckdb connection and type."""
import duckdb
from config import settings

type DdbConn = duckdb.DuckDBPyConnection

duckdb_path = settings.paths.duckdb

conn = duckdb.connect(duckdb_path)
