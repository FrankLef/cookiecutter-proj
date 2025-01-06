import pytest
import pandera as pa

from src.s0_helpers import ddict


@pytest.fixture
def a_ddict(ddict_df):
    obj = ddict.DDict(ddict_df)
    return obj


def test_ddict_shape(a_ddict):
    specs = a_ddict.get_data()
    assert specs.shape == (6, 14)


def test_ddict_err1(ddict_err1_df):
    with pytest.raises(pa.errors.SchemaError):
        ddict.DDict(ddict_err1_df)


def test_ddict_err2(ddict_err2_df):
    with pytest.raises(pa.errors.SchemaError):
        ddict.DDict(ddict_err2_df)


# @pytest.mark.skip(reason='TODO')
def test_ddict_get_ddict(df1):
    a_ddict = ddict.DDict()
    ddict_tbl = a_ddict.get_ddict(df1, table_nm="df1")
    assert ddict_tbl.shape == (3, 14)


# @pytest.mark.skip(reason='TODO')
def test_ddict_update(df1, df1a):
    a_ddict = ddict.DDict()
    a_ddict.update(df1, table_nm="df1")
    a_ddict.update(df1a, table_nm="df1")
    ddict_tbl = a_ddict.get_data()
    assert ddict_tbl.shape == (4, 14)


def test_ddict_schema(ddict_df):
    obj = ddict.DDict(ddict_df)
    schem = obj.get_schema(table="tbl1", coerce=True, strict=True)
    assert isinstance(schem, pa.api.pandas.container.DataFrameSchema)
