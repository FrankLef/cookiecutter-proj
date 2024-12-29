import pytest

from src.s0_helpers import tdict as tdict_cls


@pytest.fixture
def tdict(tdict_df):
    obj = tdict_cls.TDict(tdict_df)
    return obj

def test_tdict_shape(tdict_df):
    assert tdict_df.shape == (3, 12)
    

def test_tdict(tdict):
    specs = tdict.get_data()
    assert specs.shape == (3, 12)


def test_tdict_err(tdict):
    with pytest.raises(UserWarning):
        tdict.get_data(role="wrong")
