import pandas as pd


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
        # calc_var is the extra column that will be created
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

    def _clean_mat(self):
        # raise error when some index in data don't exist in the matrix.
        missing_id = self._audit_results["missing_id"]
        missing_id_nb = len(missing_id)
        if missing_id_nb:
            msg = f"""There are {missing_id_nb} values of {self._id_var} in
            `data` that are not found `mat`. Add them to `mat` or drop them."""
            raise ValueError(msg)
        # remove id_var that do not have enough amounts from data.
        mat_clean = self._mat
        not_todo = self._audit_results["not_todo"]
        sel = mat_clean[self._new_var].isin(not_todo)
        mat_clean.loc[sel, self._coef_var] = float("NaN")
        self._mat_clean = mat_clean

    def _audit_merge(self, tol: float = 1e-8):
        df_merged = self._mat.merge(
            right=self._data, how="outer", on=self._id_var, indicator=True
        )
        sel = (df_merged["_merge"] != "both") & (abs(df_merged[self._coef_var]) >= tol)
        df_merged_sel = df_merged.loc[sel]
        # get the variables that will be set to NaN because there is missing id_var.
        not_todo = (
            df_merged_sel.loc[df_merged_sel["_merge"] == "left_only", self._new_var]
            .unique()
            .tolist()
        )
        # get the values in data's id_vars that are not found in the mat's id_var
        sel = df_merged["_merge"] != "both"
        df_merged_sel = df_merged.loc[sel]
        missing_id = (
            df_merged_sel.loc[df_merged_sel["_merge"] == "right_only", self._id_var]
            .unique()
            .tolist()
        )
        out = {"not_todo": not_todo, "missing_id": missing_id}
        self._audit_results = out
        return out

    def calculate(self) -> pd.DataFrame:
        """Perform the sum of the products.

        Returns:
            pd.DataFrame: Results of the calculations.
        """
        self._audit_merge()
        self._clean_mat()
        out = self._mat_clean.merge(right=self._data, how="inner", on=self._id_var)
        out[self._calc_var] = out[self._coef_var] * out[self._amt_var]
        augment_group_vars = self._group_vars + [self._new_var]
        # IMPORTANT: must set min_count=1 to keep the NaN!
        # NOTE: skipna arguments is not implemented when using groupby!
        # Source: https://stackoverflow.com/questions/71515697/pandas-groupby-sum-is-not-ignoring-none-empty-np-nan-values
        out = out.groupby(by=augment_group_vars, as_index=False)[self._calc_var].sum(min_count=1)
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
