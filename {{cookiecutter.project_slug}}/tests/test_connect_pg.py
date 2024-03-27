"""Test the postgreSQL connection."""

from sqlalchemy import engine

import src.etl.connect_pg as extr


def test_engine_gp():
    out = extr.get_engine()
    assert isinstance(out, engine.base.Engine)


