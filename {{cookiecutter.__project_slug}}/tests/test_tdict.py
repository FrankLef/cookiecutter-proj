import pytest
from pathlib import Path
from src.s0_helpers import tdict as tdict_cls

from config import settings


@pytest.fixture
def tdict():
    a_path = Path(__file__).parents[1].joinpath("data")
    a_path = a_path.joinpath(settings.tdict)
    obj = tdict_cls.TDict(a_path)
    return obj


def test_tdict(tdict):
    specs = tdict.get_specs()
    assert not specs.empty


def test_tdict_err(tdict):
    with pytest.raises(ValueError):
        tdict.get_specs(role_rgx="wrong")
