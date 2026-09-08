from collections.abc import Sequence

import polars as pl
from fltk.prnt.print_msg import MsgType, print_msg
from fltk.qries.base import QryRepo
from fltk.qries.main import QryFltk


class QryUtils(QryRepo):
    def set_constraints(self, keys: Sequence[str], skip_error: bool = True) -> None:
        qr = QryFltk(conn=self.conn, table_nm=self.table_nm)
        qr.constraints.add_primary_key(keys=keys, skip_error=skip_error)

    def create_with_df(
        self, data: pl.DataFrame, is_temp: bool = False, verbose=False
    ) -> None:
        self.conn.register(view_name="data", python_object=data)
        if is_temp:
            create_sql = "CREATE OR REPLACE TEMPORARY TABLE"
        else:
            create_sql = "CREATE OR REPLACE TABLE"
        qry = f"{create_sql} {self.table_nm} AS SELECT * FROM data;"
        self.conn.sql(qry)
        if not verbose:
            print_msg(f"Create table {self.table_nm}", type=MsgType.INFO)
