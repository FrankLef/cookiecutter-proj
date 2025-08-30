import duckdb as ddb
from os import getlogin
from config import settings

import src.s0_helpers.richtools as rt

duckdb_path = settings.paths.duckdb


def show_ddb(tbl: str = "%", is_stop: bool = True) -> None:
    qry = f"SELECT * FROM (SHOW TABLES) WHERE name like '{tbl}'"
    with ddb.connect(duckdb_path) as conn:
        tbl_nms = conn.sql(qry).fetchall()
        for tbl_nm in tbl_nms:
            nm = tbl_nm[0]
            nrows = conn.sql(f"SELECT count(*) as nb FROM {nm}").fetchone()[0]  # type: ignore
            rt.print_msg(f"{nm} with {nrows} rows.", type="info")
            conn.sql(f"DESCRIBE {nm}").show()
    if is_stop:
        rt.print_msg(f"Process stopped by user '{getlogin()}'.", type="fail")
        raise KeyboardInterrupt()


def set_constraints(
    conn: ddb.DuckDBPyConnection, tbl: str, pk: list[str], notnull: list[str]
) -> None:
    pk_csv = ",".join(pk)  # type: ignore
    qry = f"ALTER TABLE {tbl} ADD PRIMARY KEY ({pk_csv})"
    conn.sql(qry)

    for col in notnull:  # type: ignore
        qry = f"ALTER TABLE {tbl} ALTER COLUMN {col} SET NOT NULL"
        conn.sql(qry)
