"""
Manage files and directories.

Normally this script stays with the module.
"""

from pathlib import Path

from config import settings

from src.s0_helpers import path_finder as pfr

data_paths = settings.data_paths
data_path = Path(__file__).parents[2].joinpath("data")

pathfindr = pfr.PathFinder(paths=data_paths, base_path=data_path)