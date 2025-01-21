import pandas as pd


class CalcRatio:
    """Calculate the quotient to create new ratios."""
    
    TERMS_NM = ['den', 'num']

    def __init__(
        self, defs: pd.DataFrame, id_var: str, new_var: str, quotient_var: str, calc_var: str
    ):
        """Data frame (in long form) defining the ratios.

        Args:
            defs (pd.DataFrame): Data frame in long form of ratio definitions.
            id_var (str): Variable used to join the definition with the data.
            new_var (str): Name of new variable (ratio).
            quotient_var (str): Name of the column containing 'num' and 'den'.
            calc_var (str): Name of new amount created by the ratio.
        """
        self._defs = defs
        self._id_var = id_var
        self._new_var = new_var
        self._quotient_var = quotient_var
        self._calc_var = calc_var
        self._validate_defs()

    def _validate_defs(self) -> bool:
        """Validate the data frame of ratio definitons.

        Raises:
            ValueError: The defs data frame is empty.
            TypeError: A variable name is empty.
            KeyError: A variable name is not a columne of `defs`.
            TypeError: `calc_var` is empty.
            ValueError: The terms 'num' and 'den' are not found.

        Returns:
            bool: True if all validation are ok.
        """
        if self._defs.empty:
            raise ValueError("`defs` must not be empty.")
        vars = {
            'id_var': self._id_var,
            'new_var': self._new_var,
            'quotient_var': self._quotient_var,
        }
        for key, val in vars.items():
            if not val:
                raise TypeError(f"`{key}` is an empty string.")
            if val not in self._defs.columns:
                raise KeyError(f"'{val}' is not a column of `defs`.")
        if not self._calc_var:
            raise TypeError(f"`{self._calc_var}` is an empty string.")
        the_terms = sorted(self._defs[self._quotient_var].unique().tolist())
        terms_nm = type(self).TERMS_NM
        if the_terms != terms_nm:
            msg = f"The terms in '{self._quotient_var}' are not in {terms_nm}."
            raise ValueError(msg)
        return True

    def _validate_data(
        self, data: pd.DataFrame, id_var: str, amt_var: str, group_vars: list[str]
    ) -> bool:
        if data.empty:
            raise ValueError("`data` must not be empty.")
        # check the id_var
        if id_var != self._id_var:
            msg = f"""The data's id_var '{id_var}' must be the same as the defs' `id_var` which is '{self._id_var}'"""
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

    def calculate(self, drop_na: bool) -> pd.DataFrame:
        
        out = self._defs.merge(right=self._data, on=self._id_var)
        self._data_merged = out
        
        cols = [self._new_var] + self._group_vars
        terms_nm = type(self).TERMS_NM
        eval_str = f"{self._calc_var} = {terms_nm[1]} / {terms_nm[0]}"
        out = (
            out
            .drop(columns=self._id_var)
            .pivot(index=cols, columns=self._quotient_var, values=self._amt_var)
            .eval(eval_str)
            .reset_index()
            )

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
            # NOTE: No need to assign `id_var` as it should be in mat already.
            self._data = data
            self._amt_var = amt_var
            self._group_vars = group_vars
            # NOTE: The data must contains only the relevant columns.
            cols = [self._id_var, self._amt_var] + group_vars
            self._data = data[cols]
        else:
            msg = "Validation of `data` failed."
            raise RuntimeError(msg)


    @property
    def defs(self):
        """The original definitions."""
        return self._defs

    @property
    def data(self):
        """The original input data."""
        return self._data

    @property
    def data_merged(self):
        """For debuging. Merged data with calculations."""
        return self._data_merged
