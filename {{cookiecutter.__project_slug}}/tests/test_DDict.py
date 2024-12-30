import pytest

from src.s0_helpers import ddict


@pytest.fixture
def a_ddict(ddict_df):
    obj = ddict.DDict(ddict_df)
    return obj


def test_ddict_shape(a_ddict):
    specs = a_ddict.get_data()
    assert specs.shape == (6, 11)


def test_ddict_err1(ddict_err1_df):
    rgx = r"There are 1 duplicated values in 'raw_name' and 1 values in 'name'[.]"
    with pytest.raises(ValueError, match=rgx):
        ddict.DDict(ddict_err1_df)


def test_ddict_err2(ddict_err2_df):
    rgx = r"2 NA values in the 'raw_name' column[.]"
    with pytest.raises(ValueError, match=rgx):
        ddict.DDict(ddict_err2_df)

def test_ddict_get_ddict(df1):
    a_ddict = ddict.DDict()
    ddict_tbl = a_ddict.get_ddict(df1, table_nm="df1")
    assert ddict_tbl.shape == (3, 11)
    
def test_ddict_update(df1, df1a):
    a_ddict = ddict.DDict()
    a_ddict.update(df1, table_nm="df1")
    a_ddict.update(df1a, table_nm="df1")
    ddict_tbl = a_ddict.get_data()
    assert ddict_tbl.shape == (4, 11)