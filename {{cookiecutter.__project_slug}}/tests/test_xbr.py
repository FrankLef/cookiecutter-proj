"""Test the xbr classes."""

import pytest
import src.s0_helpers.cls.xbr as xbr


@pytest.fixture
def some_items():
    item0 = xbr.XbrColumn(
        name="item0",
        label="The label for item0",
        roles={"pk", "nn"},
        dtype="VARCHAR",
    )
    item1 = xbr.XbrValue(
        name="item1",
        label="The label for item1",
        roles={"pk"},
    )
    item2 = xbr.XbrValue(name="item2")
    return {"item0": item0, "item1": item1, "item2": item2}


@pytest.fixture
def some_containers(some_items):
    container0 = xbr.XbrContainer(name="container0", roles={"pk", "nn"})
    container0.items = some_items
    container1 = xbr.XbrContainer(name="container1", roles={"pk"})
    container1.items = some_items
    container2 = xbr.XbrContainer(name="container2", roles={"nn"})
    container2.items = some_items
    container3 = xbr.XbrContainer(name="container3")
    container3.items = some_items
    return (container0, container1, container2, container3)


def test_empty_name():
    """Empty item name must raise a ValueError."""
    with pytest.raises(ValueError):
        xbr.XbrValue(name="")


@pytest.mark.parametrize("name", ("item X", "item-X"))
def test_invalid_name(name):
    """Invalid item name. Must have only non-word characters."""
    with pytest.raises(ValueError):
        xbr.XbrValue(name=name)


def test_invalid_roles():
    """Invalid item roles. Sould not have non-word character."""
    with pytest.raises(ValueError):
        xbr.XbrValue(name="itemX", roles={"pk.nn"})


def test_dupl_name(some_containers, some_items):
    """Duplicate item names."""
    the_item = some_items["item0"]
    a_container = some_containers[0]
    with pytest.raises(UserWarning):
        a_container.add(the_item)


def test_invalid_role(some_containers):
    """Invalid role. Sould not have non-word character."""
    a_container = some_containers[0]
    a_container.roles = {"pk", "nn"}
    with pytest.raises(ValueError):
        a_container.get_names(roles={"nk.nn"})


def test_wrong_role(some_containers):
    """Number of items using the user-defined roles is zero."""
    a_container = some_containers[1]
    with pytest.raises(AssertionError):
        a_container.get_names(roles={"error"})


the_test_params = (
    [3, set(), ["item0", "item1", "item2"]],
    [1, set(), ["item0", "item1"]],
    [1, {"nn"}, ["item0"]],
)


@pytest.mark.parametrize("container_no, roles, expected", the_test_params)
def test_get_names_with_roles(some_containers, container_no, roles, expected):
    """Get the names of all items, i.e. with roles."""
    a_container = some_containers[container_no]
    the_target = expected
    the_names = a_container.get_names(roles)
    assert the_names == the_target


def test_csv(some_containers):
    """Test container's csv string."""
    a_container = some_containers[3]
    the_values = ["item0", "item1", "item2"]
    the_target = ",".join(the_values)
    the_text = a_container.write_csv()
    assert the_text == the_target


def test_sql(some_containers):
    """Test container's sql string."""
    a_container = some_containers[3]
    the_values = ["item0 AS VARCHAR", "'item1'", "'item2'"]
    the_target = ",".join(the_values)
    the_text = a_container.write_sql()
    assert the_text == the_target
