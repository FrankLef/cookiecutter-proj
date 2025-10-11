"""Test the xbr classes."""

import pytest
from dataclasses import dataclass, fields
from src.s0_helpers.xbr.xbr_group import IXbrAttr, IXbrUnit, IXbrGroup


@dataclass
class XbrAttr1(IXbrAttr):
    pass


@dataclass
class XbrAttr2(IXbrAttr):
    extra: int | None = None


@dataclass
class XbrUnit1(IXbrUnit):
    field1: str
    field2: str
    field3: str

    @property
    def attrs(self) -> list[XbrAttr1]:
        out = [
            XbrAttr1(name=self.field1, rule="pk"),
            XbrAttr1(name=self.field2, rule="pk", role="r1"),
            XbrAttr1(name=self.field3, rule="nn", role="r1,r2"),
        ]
        return out


@dataclass
class XbrUnit2(IXbrUnit):
    field1: str
    field2: str
    field3: str
    field4: str

    @property
    def attrs(self) -> list[XbrAttr2]:
        out = [
            XbrAttr2(name=self.field1, rule="pk", role="r1"),
            XbrAttr2(name=self.field2, rule="pk", role="r2"),
            XbrAttr2(name=self.field3, rule="nn", role="r1,r2"),
            XbrAttr2(name=self.field4),
        ]
        return out


@dataclass
class XbrGroup(IXbrGroup):
    xbr1: XbrUnit1
    xbr2: XbrUnit2


@pytest.fixture
def xbr1_inst(xbr1):
    xbr_unit = XbrUnit1(**xbr1)
    return xbr_unit


@pytest.fixture
def xbr2_inst(xbr2):
    xbr_unit = XbrUnit2(**xbr2)
    return xbr_unit


@pytest.fixture
def group_inst(xbr1_inst, xbr2_inst):
    xbr_group = XbrGroup(name="main_group", xbr1=xbr1_inst, xbr2=xbr2_inst)
    return xbr_group


def test_inst1(xbr1_inst):
    the_fields = fields(xbr1_inst)
    # print(xbr1_inst)
    assert len(the_fields) == 4


def test_inst2(xbr2_inst):
    the_fields = fields(xbr2_inst)
    # print(the_fields)
    assert len(the_fields) == 5


def test_attrs1_size(xbr1_inst):
    assert len(xbr1_inst.attrs) == len(fields(xbr1_inst)) - 1


def test_attrs2_size(xbr2_inst):
    assert len(xbr2_inst.attrs) == len(fields(xbr2_inst)) - 1


def test_rule1_err(xbr1_inst):
    with pytest.raises(KeyError):
        xbr1_inst.get_rule(name="x")


@pytest.mark.parametrize(
    "rule, expected",
    (
        ["pk", ["value1", "value2"]],
        ["nn", "value3"],
    ),
)
def test_rules1(xbr1_inst, rule, expected):
    rules = xbr1_inst.get_rule(rule)
    assert rules == expected


@pytest.mark.parametrize(
    "role, expected",
    (
        ["r1", ["value2", "value3"]],
        ["r2", "value3"],
    ),
)
def test_roles1(xbr1_inst, role, expected):
    roles = xbr1_inst.get_role(role)
    assert roles == expected


def test_group_size(group_inst):
    assert len(fields(group_inst)) == 3


def test_group_sql(xbr1_inst, group_inst):
    rule = xbr1_inst.get_rule(name="pk")
    rule_sql = group_inst.write_sql(rule)
    expected = "'value1','value2'"
    assert rule_sql == expected
