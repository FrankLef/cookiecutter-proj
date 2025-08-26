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


def test_lines(dictbl1):
    a_line = dictbl1.lines[0]
    assert isinstance(a_line,TestDicLine)


@pytest.mark.parametrize("txt, target, expected", [
    ["tbl", "tbl", True],
    ["tbl", "", False],
    ["", "tbl", True],
    ["", "", True],
    ["val1", "val1,val2", True],
    ["val3", "val1,val2", False]
])
def test_check_txt(dictbl1, txt, target, expected):
    a_line = dictbl1.lines[0]
    out = a_line.check_txt(txt=txt, target=target)
    assert out == expected


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
