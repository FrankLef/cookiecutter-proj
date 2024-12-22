import pytest
from pathlib import Path
from src.s0_helpers import path_finder as pfr

from config import settings

@pytest.fixture
def data_paths():
    return settings.data_paths

@pytest.fixture
def data_path():
    a_path = Path(__file__).parents[1].joinpath("data")
    return a_path


# @pytest.mark.skip
def test_get_data_path(data_paths, data_path, id="raw"):
    pathfindr = pfr.PathFinder(paths=data_paths, base_path=data_path)
    a_path = pathfindr.get_path(id=id)
    target = Path(__file__).parents[1].joinpath("data", "d1_raw")
    assert a_path == target


def test_get_data_path_keyerr(data_paths, data_path,id="wrong"):
    pathfindr = pfr.PathFinder(paths=data_paths, base_path=data_path)
    with pytest.raises(KeyError):
        pathfindr.get_path(id=id)


def test_get_data_path_direrr(data_paths, data_path, id="raw", sub="wrong"):
    pathfindr = pfr.PathFinder(paths=data_paths, base_path=data_path)
    with pytest.raises(NotADirectoryError):
        pathfindr.get_path(id=id, sub=sub)