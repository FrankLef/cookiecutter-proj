"""
Manage files and directories.

Normally this script stays with the module.
"""

from pathlib import Path

from config import settings

from src.s0_helpers import path_finder as pathfinder_cls
from src.s0_helpers import tdict as tdict_cls
from src.s0_helpers import file_namer as fnamer_cls


data_paths = settings.data_paths
data_path = Path(__file__).parents[2].joinpath("data")

# the PathFinder instance used in the project
pathfindr = pathfinder_cls.PathFinder(paths=data_paths, base_path=data_path)

# the TDict instance used in the project
tdict_path = data_path.joinpath(settings.tdict)
tdict = tdict_cls.TDict(tdict_path)

# the FileNamer instance used in the project
fnamer = fnamer_cls.FileNamer()