"""
Manage files and directories.

Normally this script stays with the module.
"""

from pathlib import Path

from config import settings

from src.s0_helpers import path_finder as pfr
from src.s0_helpers import tdict as tdict_cls


data_paths = settings.data_paths
data_path = Path(__file__).parents[2].joinpath("data")

# the PathFinder object used everywhere in the module to find the paths
pathfindr = pfr.PathFinder(paths=data_paths, base_path=data_path)

tdict_path = data_path.joinpath(settings.tdict)
tdict = tdict_cls.TDict(tdict_path)
