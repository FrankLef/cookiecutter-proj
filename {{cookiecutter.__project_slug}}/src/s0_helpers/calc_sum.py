import pandas as pd
import numpy as np


class CalcSum:
    """Calculate the product and sum to create new amounts."""

    def __init__(
        self,
        defs: pd.DataFrame,
        id_var: str,
        new_var: str,
        coef_var: str,
        calc_var: str,
    ):
        """Data frame (in long form) defining the sum of products.

        Args:
            defs (pd.DataFrame): Matrix in long form.
            id_var (str): Variable used to join the matrix with the data.
            new_var (str): Name of new variable created by the calculations.
            coef_var (str): Name of variable with the coefficients used.
            calc_var (str): Name of new amount created by the sum product.
        """
        self._defs = defs
        self._id_var = id_var
        self._new_var = new_var
        self._coef_var = coef_var
        self._calc_var = calc_var
        self._validate_defs()

    def _validate_defs(self) -> bool:
        """Validate the definitions data frame.

        Raises:
            ValueError: The matrix is empty.
            TypeError: A variable name is empty.
            KeyError: A variable name is not a columns of `defs`.
            TypeError: `calc_var` is empty.

        Returns:
            bool: True if all validation are ok.
        """
        if self._defs.empty:
            raise ValueError("`defs` must not be empty.")
        vars = {
            "id_var": self._id_var,
            "new_var": self._new_var,
            "coef_var": self._coef_var,
        }
        for key, val in vars.items():
            if not val:
                raise TypeError(f"`{key}` is an empty string.")
            if val not in self._defs.columns:
                raise KeyError(f"'{val}' is not a column of `defs`.")
        if not self._calc_var:
            raise TypeError(f"`{self._calc_var}` is an empty string.")
        return True

    def _validate_data(
        self, data: pd.DataFrame, id_var: str, amt_var: str, group_vars: list[str]
    ) -> bool:
        if data.empty:
            raise ValueError("`data` must not be empty.")
        # check the id_var
        if id_var != self._id_var:
            msg = f"""The data's id_var '{id_var}' must be the same as the defs' id_var which is '{self._id_var}'"""
            raise KeyError(msg)
        vars = {"id_var": id_var, "amt_var": amt_var}
        for key, val in vars.items():
            if not val:
                msg = f"`{key}` is an empty string."
                raise TypeError(msg)
            if val not in data.columns:
                msg = f"'{val}' is not in the columns of `data`."
                raise KeyError(msg)
        vars = {
            "new_var": self._new_var,
            "coef_var": self._coef_var,
            "calc_var": self._calc_var,
        }
        for key, val in vars.items():
            if val in data.columns:
                msg = f"""The column name '{val}' is in `defs` as well as in `data`. It must be found in only one of the two."""
                raise KeyError(msg)
        # check the group variables
        err_if = [x not in data.columns for x in group_vars]
        err_nb = sum(err_if)
        if err_nb:
            msg = f"`group_vars` has {err_nb} variables not found in `data` columns."
            raise KeyError(msg)
        return True

    def calculate(
        self, sum_na: bool, drop_na: bool, tol: float = 1e-8
    ) -> pd.DataFrame:
        """Calculate the sumproduct of the data with the given matrix.

        The `with_na` argument is very important. See the notebook 'calcsum01a.ipynb' for more details.

        If `sum_na=True` then `NaN` will replace missing data and the `sum` will return `NaN` when there is missing data.
        
        If `sum_na=False` then `sum` will assume the missing data is equivalent to zero.

        If you want to have sum of chronological data, i.e. consider missing data as zero, then you should use `sum_na=False`.  In this case, check
        the results, very often the last period will be incorrect and should
        be removed.

        Args:
            sum_na (bool): If True, `NaN` propagate with `sum`. See details.
            drop_na (bool): If True, drop `NaN` rows from final result.
            tol (float, optional): Tolerance. Defaults to 1e-8.

        Returns:
            pd.DataFrame: Data frame of resulting computations.
        """
        self._rm_missing_new_var()
        defs_clean = self._defs_clean
        if sum_na:
            out = self._set_data_na()
        else:
            out = self._data

        out = defs_clean.merge(right=out, how="inner", on=self._id_var)

        # IMPORTANT: Must remove zero from matrix column to avoid all NaN by row in the result.
        sel = abs(out[self._coef_var]) < tol
        out.drop(index=out[sel].index, inplace=True)

        # do the multiply
        out[self._calc_var] = out[self._coef_var] * out[self._amt_var]

        # save the merged data fro DEBUG
        self._data_merged = out

        augment_group_vars = self._group_vars + [self._new_var]

        # NOTE: another way to do it.
        # SOURCE: https://stackoverflow.com/questions/18429491/pandas-groupby-columns-with-nan-missing-values (at th end)
        # dfgrouped = out.groupby(by=augment_group_vars, as_index=False)[self._calc_var].agg(['sum','size','count'])
        # dfgrouped['sum'][dfgrouped['size']!=dfgrouped['count']] = float('NaN')

        if sum_na:
            # NOTE: To have sum return NaN as soon as there is any in a group
            # the np. sum with an array MUST be used!
            # source: https://github.com/pandas-dev/pandas/issues/15674
            out = out.groupby(by=augment_group_vars, as_index=False)[
                self._calc_var
            ].apply(lambda x: np.sum(np.array(x)))
        else:
            # NOTE: Finally, Must treat the missing values as zeros for finance
            out = out.groupby(by=augment_group_vars, as_index=False)[
                self._calc_var
            ].sum()
        if drop_na:
            out.dropna(subset=self._calc_var, inplace=True)
        return out

    def set_data(
        self, data: pd.DataFrame, id_var: str, amt_var: str, group_vars: list[str]
    ):
        is_ok = self._validate_data(
            data, id_var=id_var, amt_var=amt_var, group_vars=group_vars
        )
        if is_ok:
            # NOTE: No need to assign `id_var` as it should be in defs already.
            self._data = data
            self._amt_var = amt_var
            self._group_vars = group_vars
        else:
            msg = "Validation of `data` failed."
            raise RuntimeError(msg)
        self._set_data_na()

    def _set_data_na(self):
        # format wide to create the NaN when data is missing
        data_na_wide = self._data.pivot(
            index=self._group_vars, columns=self._id_var, values=self._amt_var
        )
        data_na_wide = data_na_wide.reset_index()
        # format long to get the original dat but with NaN when values are missing
        data_na = data_na_wide.melt(
            id_vars=self._group_vars, var_name=self._id_var, value_name=self._amt_var
        )
        data_na = data_na.reset_index()
        data_na.drop(columns="index", inplace=True)
        return data_na

    def _find_missing_vars(self, tol: float = 1e-8):
        mat_merged = self._defs.merge(
            right=self._data, how="left", on=self._id_var, indicator=True
        )
        sel = (mat_merged["_merge"] == "left_only") & (
            abs(mat_merged[self._coef_var]) < tol
        )
        mat_merged = mat_merged[sel]
        miss_id = mat_merged[self._id_var].unique().tolist()
        miss_new_var = mat_merged[self._new_var].unique().tolist()
        missing_vars = {"id": miss_id, "new_var": miss_new_var}
        self._missing_vars = missing_vars

    def _rm_missing_new_var(self):
        self._find_missing_vars()
        missing_new_var = self._missing_vars["new_var"]
        defs_clean = self._defs
        if missing_new_var:
            sel = defs_clean[self._new_var].isin(missing_new_var)
            defs_clean.drop(index=defs_clean[sel].index, inplace=True)
        self._defs_clean = defs_clean

    @property
    def defs(self):
        """The original definitions."""
        return self._defs

    @property
    def defs_clean(self):
        """For debugging. Definitions with non-existing `new_var` removed."""
        self._rm_missing_new_var()
        return self._defs_clean

    @property
    def missing_vars(self):
        """Dictionary of missing variables."""
        self._find_missing_vars()
        return self._missing_vars

    @property
    def data(self):
        """The original input data."""
        return self._data

    @property
    def data_merged(self):
        """For debuging. Merged data with calculations, before summing it."""
        return self._data_merged
