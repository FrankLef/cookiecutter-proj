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

    def calculate(self, drop_na: bool, with_na:bool, tol: float = 1e-8) -> pd.DataFrame:
        """Calculate the sumproduct of the data with the given matrix.add()
        
        The `with_na` argument is very important.
        
        If you wnats sums of amounts, you should use `with_na=True` to make sure NaN will be put where to replace missing data and make the aum not add any variable where missing data is.
        
        If you want to have sum of chronological data, i.e. consider missing data as zero, then you should use `with_na=False`.  In this case, check
        the results, very often the last period will be incorrect and should
        be removed.

        Args:
            drop_na (bool): Drop NaN rows from the reult.
            with_na (bool): Should the data replace missing with NaN.
            tol (float, optional): _description_. Defaults to 1e-8.

        Returns:
            pd.DataFrame: Resulting computations.
        """
        if with_na:
            out = self._data_na
        else:
            out = self._data
        
        out = self._mat.merge(right=out, how="inner", on=self._id_var)

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
        
        
        # NOTE: To have sum return NaN as soon as there is any in a group
        # the np. sum with an array MUST be used!
        # source: https://github.com/pandas-dev/pandas/issues/15674
        out = out.groupby(by=augment_group_vars, as_index=False)[self._calc_var].apply(
            lambda x: np.sum(np.array(x))
        )

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
        self._set_data_na()
        
        
    def _set_data_na(self):
        # format wide to create the NaN when data is missing
        data_na_wide = self._data.pivot(
            index=self._group_vars, columns=self._id_var, values=self._amt_var)
        data_na_wide = data_na_wide.reset_index()
        # format long to get the original dat but with NaN when values are missing
        data_na = data_na_wide.melt(
            id_vars=self._group_vars, var_name=self._id_var, value_name=self._amt_var)
        data_na = data_na.reset_index()
        data_na.drop(columns='index', inplace=True)
        self._data_na = data_na


    @property
    def mat(self):
        """The origin input matrix."""
        return self._mat

    @property
    def data(self):
        """The original input data."""
        return self._data
    
    @property
    def data_na(self):
        """The input data augmented with naN when a value is missing.
        
        This is because we ABSOLUTELY need NaN whenever a value is missing
        when doing the join in `calculate`.
        """
        return self._data_na
    
    @property
    def data_merged(self):
        return self._data_merged
