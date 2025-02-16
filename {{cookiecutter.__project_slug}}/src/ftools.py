"""Tools to manipulate files."""

from pathlib import Path
import pandas as pd
from functools import partial

from config import settings

data_paths = settings.data_paths
data_path = settings.paths.data


def pathfindr(id: str, *other: str) -> Path:
    if id in data_paths.keys():
        path = data_path.joinpath(data_paths[id])
        path = path.joinpath(*other)
    else:
        raise KeyError(f"'{id}' is an invalid data path id.")
    if not path.exists():
        raise FileExistsError(f"{path} does not exist.")
    return path


def fnamer(name: str, *suffix, ext: str):
    SEP = "_"
    if not name:
        raise ValueError("A file name must be provided.")
    a_join = (name,) + suffix
    fn = SEP.join(a_join) + ext
    return fn


fnamer_pkl = partial(fnamer, ext=".pkl")
fnamer_xl = partial(fnamer, ext=".xlsx")


def read_pkl(path: Path, name: str, suffix: str | None = None) -> pd.DataFrame:
    """Build a file name and read it with pickle.

    Args:
        path (Path): Path where file is located.
        name (str): The stem of the file name.
        suffix (str | None, optional): Suffix to file name. Defaults to None.

    Returns:
        pd.DataFrame: Data frame.
    """
    if suffix is not None:
        fn = fnamer_pkl(name, suffix)
    else:
        fn = fnamer_pkl(name)
    path_fn = path.joinpath(fn)
    out = pd.read_pickle(path_fn)
    assert not out.empty, "Input data must not be empty."
    return out


def write_pkl(
    data: pd.DataFrame, path: Path, name: str, suffix: str | None = None
) -> Path:
    """Build a file name and write it with pickle.

    Args:
        data (pd.DataFrame): Data frame.
        path (Path): Path where file is located.
        name (str): The stem of the file name.
        suffix (str | None, optional): Suffix to file name. Defaults to None.

    Returns:
        Path: Data frame.
    """
    assert not data.empty, "Output data must not be empty."
    if suffix is not None:
        fn = fnamer_pkl(name, suffix)
    else:
        fn = fnamer_pkl(name)
    path_fn = path.joinpath(fn)
    data.to_pickle(path_fn)
    return path_fn


def read_xl(
    path: Path, name: str, suffix: str | None = None, sheet_nm: str | int = 0
) -> pd.DataFrame:
    """Build a file name and read it with excel.

    Args:
        path (Path): Path where file is located.
        name (str): The stem of the file name.
        suffix (str | None, optional): Suffix to file name. Defaults to None.
        sheet_nm (str | int, optional): Sheet name or number. Defaults to 0.

    Returns:
        pd.DataFrame: Data frame.
    """
    if suffix is not None:
        fn = fnamer_xl(name, suffix)
    else:
        fn = fnamer_xl(name)
    path_fn = path.joinpath(fn)
    out = pd.read_excel(path_fn, sheet_name=sheet_nm)
    assert not out.empty, "Input data must not be empty."
    return out


def write_xl(
    data: pd.DataFrame,
    path: Path,
    name: str,
    suffix: str | None = None,
    sheet_nm: str = "Sheet1",
    with_index: bool = False,
) -> Path:
    """Build a file name and write it with excel.

    Args:
        data (pd.DataFrame): Data frame.
        path (Path): Path where file is located.
        name (str): The stem of the file name.
        suffix (str | None, optional): Suffix to file name. Defaults to None.
        sheet_nm (str, optional): Sheet name. Defaults to "Sheet1".
        with_index (bool, optional): Write index. Defaults to False.

    Returns:
        Path: Data frame.
    """
    assert not data.empty, "Output data must not be empty."
    if suffix is not None:
        fn = fnamer_xl(name, suffix)
    else:
        fn = fnamer_xl(name)
    path_fn = path.joinpath(fn)
    data.to_excel(path_fn, sheet_name=sheet_nm, index=with_index)
    return path_fn
