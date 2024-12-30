import pytest
import pandas as pd
import json
from pathlib import Path

# https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest


@pytest.fixture
def data_paths():
    with open("tests/fixtures/data_paths.json") as f:
        out = json.load(f)
    return out


@pytest.fixture
def data_path():
    a_path = Path(__file__).parents[1].joinpath("data")
    return a_path

@pytest.fixture
def tdict_df():
    df = pd.read_json("tests/fixtures/tdict.json")
    return df


@pytest.fixture
def ddict_df():
    df = pd.read_json("tests/fixtures/ddict.json")
    return df

@pytest.fixture
def ddict_err1_df():
    df = pd.read_json("tests/fixtures/ddict_err1.json")
    return df

@pytest.fixture
def ddict_err2_df():
    df = pd.read_json("tests/fixtures/ddict_err2.json")
    return df