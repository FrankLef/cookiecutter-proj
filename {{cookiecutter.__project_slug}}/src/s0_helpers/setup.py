"""
Manage files and directories.

Normally this script stays with the module.
"""
import pandas as pd
from config import settings

from src.s0_helpers import tdict, path_finder, file_namer

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
