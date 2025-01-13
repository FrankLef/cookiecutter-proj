import pandas as pd
import numpy as np


class CalcSum:
    """Calculate the product and sum to create new amounts."""

    def __init__(
        self, mat: pd.DataFrame, id_var: str, new_var: str, coef_var: str, calc_var: str
    ):
        """Matrix (in long form) that will be used to do the sum of products.

        Args:
            mat (pd.DataFrame): Matrix in long form.
            id_var (str): Variable used to join the matrix with the data.
            new_var (str): Name of new variable created by the calculations.
            coef_var (str): Name of variable with the coefficients used.
            calc_var (str): Name of new amount created by the sum product.
        """
        self._mat = mat
        self._id_var = id_var
        self._new_var = new_var
        self._coef_var = coef_var
        self._calc_var = calc_var
        self._validate_mat()

    def _validate_mat(self) -> bool:
        """Validate matrix for CalcSum.

        Raises:
            ValueError: The matrix is empty.
            TypeError: A variable name is empty.
            KeyError: A variable name is not in the matrix.`
            TypeError: `calc_var` is empty.

        Returns:
            bool: _description_
        """
        if self._mat.empty:
            raise ValueError("`mat` must not be empty.")
        vars = {
            "id_var": self._id_var,
            "new_var": self._new_var,
            "coef_var": self._coef_var,
        }
        for key, val in vars.items():
            if not val:
                msg = f"`{key}` is an empty string."
                raise TypeError(msg)
            if val not in self._mat.columns:
                msg = f"'{val}' is not in the columns of `mat`."
                raise KeyError(msg)
        # calc_var is the extra column that will have the new amounts.
        if not self._calc_var:
            msg = f"`{self._calc_var}` is an empty string."
            raise TypeError(msg)
        return True

    def _validate_data(
        self, data: pd.DataFrame, id_var: str, amt_var: str, group_vars: list[str]
    ) -> bool:
        if data.empty:
            raise ValueError("`data` must not be empty.")
        # check the id_var
        if id_var != self._id_var:
            msg = f"""The data's id_var '{id_var}' must be the same as the mat's id_var which is '{self._id_var}'"""
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
                msg = f"""The column name '{val}' is in `mat` as well as in `data`. It must be found in only one of the two."""
                raise KeyError(msg)
        # check the group variables
        err_if = [x not in data.columns for x in group_vars]
        err_nb = sum(err_if)
        if err_nb:
            msg = f"`group_vars` has {err_nb} variables not found in `data` columns."
            raise KeyError(msg)
        return True


    def calculate(self, drop_na: bool, tol:float=1e-8) -> pd.DataFrame:
        """Perform the sum of the products.

        Args:
            drop_na (bool): Drop the rows where `calc_var` is `NaN`.

        Returns:
            pd.DataFrame: Results of the calculations.
        """
        out = self._mat.merge(right=self._data, how='inner', on=self._id_var)
        
        # IMPORTANT: Must remove zero from matrix column to avoid all NaN by row in the result.
        sel = abs(out[self._coef_var]) < tol
        out.drop(index=out[sel].index, inplace=True)
        
        # do the multiply
        out[self._calc_var] = out[self._coef_var] * out[self._amt_var]
        
        # NOTE: To have sum return NaN as soon as there is any in a group
        # the np. sum with an array MUST be used!
        # source: https://github.com/pandas-dev/pandas/issues/15674
        augment_group_vars = self._group_vars + [self._new_var]
        out = out.groupby(by=augment_group_vars, as_index=False)[self._calc_var].apply(lambda x: np.sum(np.array(x)))
        
        if drop_na:
            out.dropna(subset=self._calc_var, inplace=True)
        return out

    def set_data(
        self, data: pd.DataFrame, id_var: str, amt_var: str, group_vars: list[str]
    ):
        out = self._validate_data(
            data, id_var=id_var, amt_var=amt_var, group_vars=group_vars
        )
        if out:
            # NOTE: No need to assign `id_var` as it should be in mat already.
            self._data = data
            self._amt_var = amt_var
            self._group_vars = group_vars
        else:
            msg = "Validation of `data` failed."
            raise RuntimeError(msg)

    @property
    def mat(self):
        """The origin input matrix."""
        return self._mat

    @property
    def mat_clean(self):
        """The matrix net of missing index used to calculate."""
        return self._mat_clean

    @property
    def data(self):
        """The input data to multiply by the clean matrix."""
        return self._data
