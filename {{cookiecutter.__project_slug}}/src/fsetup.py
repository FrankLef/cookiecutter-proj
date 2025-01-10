"""Files, directories and connections setup.

This is the place when to instantiate the classes used throughout the project.
"""

from pathlib import Path
import pandas as pd
from config import settings

from src.s0_helpers import connect_acc, tdict, ddict, path_finder, file_namer

data_paths = settings.data_paths
data_path = settings.paths.data

# the PathFinder instance used in the project
pathfindr = path_finder.PathFinder(paths=data_paths, base_path=data_path)

# the TDict instance used in the project
tdict_path = data_path.joinpath(settings.tdict)
a_tdict = tdict.TDict(pd.read_excel(tdict_path))
a_tdict.path = tdict_path

ddict_path = data_path.joinpath(settings.ddict)
ddict_df = pd.read_excel(ddict_path)
# print(ddict_df)
# raise KeyboardInterrupt()
a_ddict = ddict.DDict(ddict_df)
a_ddict.path = ddict_path
a_ddict.audit()

# the FileNamer instances used in the project
fnamer_xl = file_namer.FileNamer(ext=".xlsx")
fnamer_pkl = file_namer.FileNamer(ext=".pkl")

# the database connections
db_path = Path(settings.db.fn)
conn_acc_db = connect_acc.ConnectAcc(path=db_path)
rawdb_path = Path(settings.raw_db.fn)
conn_acc_rawdb = connect_acc.ConnectAcc(path=rawdb_path)
