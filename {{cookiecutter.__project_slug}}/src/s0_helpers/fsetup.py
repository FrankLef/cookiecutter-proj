"""Files, directories and connections setup.

This is the place when to instantiate the classes used throughout the project.
"""

from pathlib import Path
import pandas as pd
from config import settings

from src.s0_helpers import tdict, path_finder, file_namer, connect_acc

data_paths = settings.data_paths
data_path = settings.paths.data

# the PathFinder instance used in the project
pathfindr = path_finder.PathFinder(paths=data_paths, base_path=data_path)

# the TDict instances used in the project
tdict_etl_path = data_path.joinpath(settings.tdict_etl)
tdict_etl = tdict.TDict(pd.read_excel(tdict_etl_path))
tdict_eda_path = data_path.joinpath(settings.tdict_eda)
tdict_eda = tdict.TDict(pd.read_excel(tdict_eda_path))

# the FileNamer instances used in the project
fnamer = file_namer.FileNamer()
fnamer_fea = file_namer.FileNamer(ext=".fea")

# the database connections
db_path = Path(settings.db.fn)
conn_acc_db = connect_acc.ConnectAcc(path=db_path)
rawdb_path = Path(settings.raw_db.fn)
conn_acc_rawdb = connect_acc.ConnectAcc(path=rawdb_path)