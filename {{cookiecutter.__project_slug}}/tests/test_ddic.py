"""Test the dic classes."""

import pytest
import pandas as pd
import src.s0_helpers.cls.dic as dic


class TestDicLine(dic.IDicLine):
    pass


class TestDicTable(dic.IDicTable):
    def load(self, data: pd.DataFrame):
        for row in data.itertuples():
            line = TestDicLine(
                table_nm=row.table_nm,
                name=row.name,
                raw_name=row.raw_name,
                label=row.label,
                raw_dtype=row.raw_dtype,
                dtype=row.dtype,
                activ=row.activ,
                rules=row.rules,
                roles=row.roles,
                desc=row.desc,
                note=row.note,
            )
            self.add(line)


@pytest.fixture
def dictbl1(dic1):
    out = TestDicTable(name="table1")
    out.load(data=dic1)
    return out


@pytest.mark.parametrize(
    "table_nm, expected", [["tbl1", 3], ["tbl1 ", 3], ["", 6], [None, 6], ["X", 0]]
)
def test_has_table(dictbl1, table_nm, expected):
    the_lines = [x for x in dictbl1.lines if x.has_table(table_nm)]
    assert len(the_lines) == expected


@pytest.mark.parametrize("rule, expected", [["pk", 2], ["nn", 2], ["", 6], [None, 6]])
def test_has_rule(dictbl1, rule, expected):
    the_lines = [x for x in dictbl1.lines if x.has_rule(rule)]
    assert len(the_lines) == expected


@pytest.mark.parametrize("role, expected", [["ts", 2], ["log", 1], ["", 6], [None, 6]])
def test_has_role(dictbl1, role, expected):
    the_lines = [x for x in dictbl1.lines if x.has_role(role)]
    assert len(the_lines) == expected


@pytest.mark.parametrize(
    "table_nm, rule, role, is_activ, expected",
    [
        ["tbl1", "pk", None, True, 1],
        ["", "nn", None, False, 2],
        [None, None, "ts", False, 2],
        ["tbl1", "nn", "ts", True, 1],
    ],
)
def test_get_lines(dictbl1, table_nm, rule, role, is_activ, expected):
    the_lines = dictbl1.get_lines(
        table_nm=table_nm, rule=rule, role=role, is_activ_only=is_activ
    )
    assert len(the_lines) == expected
