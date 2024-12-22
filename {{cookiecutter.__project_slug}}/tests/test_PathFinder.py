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

@pytest.fixture
def pathfindr(data_paths, data_path):
    return pfr.PathFinder(paths=data_paths, base_path=data_path)
    

# @pytest.mark.skip
def test_get_data_path(pathfindr, id="raw"):
    a_path = pathfindr.get_path(id=id)
    target = Path(__file__).parents[1].joinpath("data", "d1_raw")
    assert a_path == target


def test_get_data_path_keyerr(pathfindr, id="wrong"):
    with pytest.raises(KeyError):
        pathfindr.get_path(id=id)


def test_get_data_path_direrr(pathfindr, id="raw", sub="wrong"):
    with pytest.raises(NotADirectoryError):
        pathfindr.get_path(id=id, sub=sub)
