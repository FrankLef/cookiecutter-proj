"""Validate MS Access connection."""

# from pathlib import Path

# from config import settings

# from fltk.conn.connect_acc import ConnectAcc


# def main(db_choice: str) -> ConnectAcc:
#     match db_choice:
#         case "db":
#             path = Path(settings.db.xbr)
#         case "raw":
#             path = Path(settings.raw_db.xbr)
#         case _:
#             msg: str = f"'{db_choice}' is an invalid db choice for accdb_conn."
#             raise ValueError(msg)
#     conn = ConnectAcc(path=path)
#     return conn
