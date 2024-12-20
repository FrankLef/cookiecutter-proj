"""Multiply a dataframe and a matrix."""

import logging
import pandas as pd
# import sys

log = logging.getLogger("rich")


def main(
    data: pd.DataFrame,
    mtrx: pd.DataFrame,
    dim_var: str,
    num_var: str,
    id_vars: list[str],
    idx_var: str = "idx",
    sep: str = "<-->",
) -> pd.DataFrame:
    """Multiply a dataframe and a matrix.

    Usually used with a trial balance to compute rolling year, quartely sum, etc. It uses a matrix to reallocate amounts between a dimension variable
    which is usually a period id.

    Args:
        data (pd.DataFrame): Data frame.
        mtrx (pd.DataFrame): Sparse matrix.
        dim_var (str): Name of the dimension variable.
        num_var (str): Name of the numerical variable.
        id_vars (list[str]): List of id variable to create a unique index.
        idx_var (str, optional): String used to name the index variable. Defaults to "idx".
        sep (str, optional): Separator for the index. Defaults to "<-->".

    Raises:
        AssertionError: The variables are not all found in `data`.

    Returns:
        pd.DataFrame: Data frmae modified after multiplication with `mtrx`.
    """
    all_vars = [dim_var, num_var, *id_vars]
    check = sum([x not in data.columns for x in all_vars])
    if check:
        msg = f"{check} variables are not in the data."
        raise ValueError(msg)
    check = len(data.axes[0])
    if not check:
        msg = "Tha data is empty."
        ValueError(msg)
    mtrx = get_mtrx(mtrx, dim_var)
    # print(f"{data.info=}")
    # sys.exit(0)
    data = get_data(
        data,
        dim_var=dim_var,
        num_var=num_var,
        id_vars=id_vars,
        idx_var=idx_var,
        sep=sep,
    )
    # print(f"{data.info=}")
    # sys.exit(0)
    df = do_mult(data=data, mtrx=mtrx)
    return df


def get_mtrx(df: pd.DataFrame, dim_var: str) -> pd.DataFrame:
    assert len(df.axes[0]) >= 2, "The matrix must have at least two rows."
    assert len(df.axes[1]) >= 3, "The matrix must have at least three columns."
    if df.columns[0] != dim_var:
        msg = f"{dim_var} must be the name of the first column in the matrix."
        raise AssertionError(msg)
    check = df[dim_var].duplicated().sum()
    if not check:
        df.set_index(dim_var, inplace=True)
    else:
        # print(f"{check=}")
        raise ValueError(f"{check} duplicated values in the period index.")
    check = len(df.index.difference(df.columns))
    if check:
        msg = f"Row and column indexes have {check} different values."
        raise ValueError(msg)
    df.fillna(0, inplace=True)
    return df


def get_data(
    df: pd.DataFrame,
    dim_var: str,
    num_var: str,
    id_vars: list[str],
    idx_var: str,
    sep: str,
) -> pd.DataFrame:
    df = write_idx(df, id_vars=id_vars, idx_var=idx_var, sep=sep)
    # sort the data using the dim var to ensure it is listed in the right order in the columns
    df.sort_values(by=[dim_var], inplace=True)
    try:
        df = df.pivot(index=idx_var, columns=[dim_var], values=num_var)
    except ValueError as err:
        msg = f"Duplicate rows when doing pivot on data:\n{err}"
        raise ValueError(msg)
    df.fillna(0, inplace=True)
    return df


def write_idx(
    df: pd.DataFrame, id_vars: list[str], idx_var: str, sep: str
) -> pd.DataFrame:
    assert len(idx_var) != 0, "Index variable must be given a name."
    assert len(sep) != 0, "An index separator must be provided."

    # nb of rows in input
    nin = len(df.axes[0])

    # print(f"{df.info}")
    # sys.exit(0)
    if idx_var in df.columns:
        msg = f"'{idx_var}' must not be in the data."
        raise AssertionError(msg)

    # NOTE: Ouf!! For some reason, and extra white space was added to idx

    id_df = df[id_vars]
    idx_df = pd.DataFrame()
    for nm, col in id_df.items():
        val = col.to_list()
        val = [str(x) for x in val]
        val = [x.strip() for x in val]
        idx_df[nm] = val
    idx_df[idx_var] = idx_df.apply(lambda x: sep.join(x), axis=1)
    nout = len(idx_df.axes[0])

    if nin != nout:
        msg = f"Data has changed. Input had {nin} rows, output has {nout}."
        raise AssertionError(msg)

    # print(f"{id_df[idx_var]=}")
    # print(f"{id_df.info}")
    # sys.exit(0)
    df[idx_var] = idx_df[idx_var]
    return df


def do_mult(data: pd.DataFrame, mtrx: pd.DataFrame) -> pd.DataFrame:
    dim_max = data.columns.max()  # maximum period in data
    # print(f"{dim_max=}")
    # sys.exit(0)
    mtrx_idx = mtrx.index[mtrx.index <= dim_max]
    mtrx = mtrx.loc[mtrx_idx, mtrx_idx]
    # NOTE: This is an important check
    check = [x != y for x, y in zip(list(mtrx.index), list(data.columns))]
    check = sum(check)
    if check:
        msg = f"{check} indexes are not the same in data columns and matrix rows."
        raise AssertionError(msg)
    df = data.dot(mtrx)
    return df
