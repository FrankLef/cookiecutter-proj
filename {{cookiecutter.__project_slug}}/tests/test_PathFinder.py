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
    if not a_path.exists():
        msg = f"The Data directory not found.\n{a_path}"
        raise NotADirectoryError(msg)
    return a_path

pytest.mark.skipif(
    condition=(not data_path().exists()),
    reason="Data path must exists. Check the settings.")
@pytest.fixture
def pathfindr(data_paths, data_path):
    return pfr.PathFinder(paths=data_paths, base_path=data_path)


pytest.mark.skipif(
    condition=(not data_path().exists()),
    reason="Data path must exists. Check the settings.")
def test_get_data_path(pathfindr, id="extr"):
    a_path = pathfindr.get_path(id=id)
    target = Path(__file__).parents[1].joinpath("data", "d1_extr")
    assert a_path == target


def test_get_data_path_keyerr(pathfindr, id="wrong"):
    with pytest.raises(KeyError):
        pathfindr.get_path(id=id)


def test_get_data_path_direrr(pathfindr, id="extr", sub="wrong"):
    with pytest.raises(FileExistsError):
        pathfindr.get_path(id, sub)
