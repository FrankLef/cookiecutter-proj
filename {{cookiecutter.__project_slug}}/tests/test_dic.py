"""Test the dic classes."""

import pytest
from typing import Any
import src.s0_helpers.cls.dic as dic


class TestDicLine(dic.IDicLine):
    pass


class TestDicTable(dic.IDicTable):
    def load(self, data: dict[str, Any]):
        out = TestDicLine(
            name=data["name"],
            raw_name=data["raw_name"],
            label=data["label"],
            raw_dtype=data["raw_dtype"],
            dtype=data["dtype"],
            activ=data["activ"],
            desc=data["desc"],
            note=data["note"],
            roles=data["roles"],
        )
        self.add(out)


@pytest.fixture
def some_data():
    out = {
        "name": "lname0",
        "raw_name": "lrawname0",
        "label": "The label 0",
        "raw_dtype": "FLOAT",
        "dtype": "VARCHAR",
        "activ": True,
        "desc": "description0",
        "note": None,
        "roles": {"pk", "nn"},
    }
    return out


@pytest.fixture
def some_lines():
    the_activ = (True, True, False)
    the_roles = ({"pk", "nn"}, {"pk"}, set())
    out = [
        TestDicLine(
            name=f"lname{i}",
            raw_name=f"lrawname{i}",
            label=f"The label {i}",
            raw_dtype="FLOAT",
            dtype="VARCHAR",
            activ=the_activ[i],
            desc=f"description{i}",
            note=None,
            roles=the_roles[i],
        )
        for i in range(2)
    ]
    return out


@pytest.fixture
def table1(some_lines):
    out = TestDicTable(name="table1", lines=some_lines)
    return out


@pytest.mark.parametrize(
    "roles, expected", ([{"pk", "nn"}, True], [{"pk"}, True], [{"ab"}, False])
)
def test_has_roles(some_lines, roles, expected):
    a_line = some_lines[0]
    out = a_line.has_roles(roles)
    assert out == expected


def test_read_roles(some_lines):
    a_line = some_lines[0]
    a_line.read_roles("ab.cd,de ef")
    the_target = {"ab", "cd", "de", "ef"}
    assert a_line.roles == the_target


def test_table_activ(table1):
    the_lines = table1.get_activ_lines()
    assert len(the_lines) == 2


def test_load(some_data, some_lines):
    a_table = TestDicTable(name="tblname")
    a_table.load(data=some_data)
    a_line = some_lines[0]
    assert a_table.lines[0] == a_line
