import pandas as pd
import pandera as pa


class MMult:
    """Matrix Multiplier for Finance and BI."""

    _KEYS = ["index", "variable"]

    _SCHEMA = pa.DataFrameSchema(
        {
            "index": pa.Column(str),
            "variable": pa.Column(str),
            "value": pa.Column(float),
        },
        unique=_KEYS,
        coerce=True,
        strict=True,
    )

    def __init__(self, mat_long: pd.DataFrame):
        type(self)._SCHEMA.validate(mat_long)
        self._mat_long = mat_long.copy()
        self._to_wide()  # create matrix in wide format

    def _to_wide(self):
        mat_wide = self._mat_long.pivot(index="index", columns="variable")
        self._mat_wide = mat_wide.fillna(0)

    def mmult(self, data: pd.DataFrame):
        # check lengths
        if len(data.columns) != len(self._mat_wide.index):
            msg = f"Index and columns must have the same length. Index has length {len(self._mat_wide.index)}, columns have length {len(data.columns)}."
            raise TypeError(msg)
        # columns and index must match exactly
        err_if = data.columns != self._mat_wide.index
        err_nb = sum(err_if)
        if err_nb:
            msg = f"Column and row index must match exactly. {err_nb} invalid indexes."
            raise ValueError(msg)
        # all OK, do the matrix multiplication
        out = data.dot(self._mat_wide)
        self._data = data
        self._out = out
        return out

    @property
    def mat_wide(self):
        return self._mat_wide

    @property
    def data(self):
        return self._data

    @property
    def out(self):
        return self._out
