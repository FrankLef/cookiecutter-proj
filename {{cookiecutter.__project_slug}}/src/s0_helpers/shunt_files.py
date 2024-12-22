"""
Manage files and directories.

Normally this script stays with the module.
"""
from pathlib import Path

from config import settings

data_paths = settings.data_paths
data_path = Path(__file__).parents[2].joinpath("data")

def write_fn(name: str, *suffix, ext: str = ".xlsx", sep: str = "_") -> str:
    """Write a file name with suffix and extension."""
    assert len(name) != 0
    fn = sep.join([name, *suffix]) + ext
    return fn

def empty_dir(path: Path, pattern: str = "*") -> int:
    """Delete files matching a pattern in a directory."""
    n: int = 0
    for f in path.glob(pattern):
        if f.is_file():
            f.unlink()
            n += 1
    return n

def get_data_path(
    id: str, sub:str|None = None, name: str|None = None, 
    dct:dict[str, str]=data_paths, base_path:Path = data_path) -> Path:
    if id in dct.keys():
        a_path = base_path.joinpath(dct[id])
    else:
        msg = f"{id} is an invalid data path id."
        raise KeyError(msg)
    if sub is not None:
        a_path = a_path.joinpath(sub)
    if not a_path.is_dir():
        msg = f"{a_path} is not a directory."
        raise NotADirectoryError(msg)
    if name is not None:
        a_path = a_path.joinpath(name)
    return a_path

    