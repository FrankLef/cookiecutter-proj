import pandas as pd
import re
import numpy as np


class DDict:
    """Data dictionary with specs by variable."""

    def __init__(self, data: pd.DataFrame):
        """Data dictionary

        Args:
            data (pd.DataFrame): Data dictionary in a data frame.

        Raises:
            ValueError: Required columns are missing.
        """
        
        self._data = data
        self._validate_columns()
        self._trim()
        self._repl_ws()
        self._validate_null(cols = ["table", "raw_name", "name"])
        self._validate_uniq()
    
    def _validate_columns(self):
        self._data.columns = self._data.columns.str.lower()  # must be in lower case
        cols = {
            "table": str, "raw_name": str, "name": str, "label": str, "raw_dtype": str, "dtype": str, "role": str, "process": str, "rule": str, "desc": str, "note": str}
        err_nb = sum([x not in self._data.columns for x in cols.keys()])
        if err_nb:
            raise ValueError(f"{err_nb} required columns missing in the data.")
        else:
            self._data = self._data.astype(cols)
            
    def _trim(self):
        self._data = self._data.apply(lambda x: x.str.strip())
        
    def _repl_ws(self):
        self._data = self._data.apply(lambda x: x.replace(r'^\s*$|^None$', np.NaN, regex=True))
        # self._data.fillna("", inplace=True)
    
    def _validate_null(self, cols: list[str]):
        # print(self._data)
        for nm in cols:
            err_nb = sum(self._data[nm].isna())
            # print(nm, err_nb)
            if err_nb:
                raise ValueError(f"{err_nb} NA values in the '{nm}' column.")
    
    def _validate_uniq(self):
        raw_name_col = self._data["table"] + self._data["raw_name"]
        name_col = self._data["table"] + self._data["name"]
        raw_name_nb = raw_name_col.duplicated().sum()
        name_nb = name_col.duplicated().sum()
        if raw_name_nb | name_nb:
            msg = f"There are {raw_name_nb} duplicated values in 'raw_name' and {name_nb} values in 'name'."
            raise ValueError(msg)
        
    def get_data(
        self,
        role: str | None = None,
        process: str | None = None,
        rule: str | None = None,
        is_bound: bool = True,
    ) -> pd.DataFrame:
        """Get filtered data from a data dictionary.

        Args:
            role (str | None, optional): Regex for the role. Defaults to None.
            process (str | None, optional): Regex for the process. Defaults to None.
            rule (str | None, optional): Regex for the rule. Defaults to None.
            is_bound (bool, optional): Add regex boundaries. Defaults to True.

        Raises:
            UserWarning: The filtered data frame is empty.

        Returns:
            pd.DataFrame: Filtered data in a data frame.
        """
        role_sel = self._find_rows(var="role", val=role, is_bound=is_bound)
        process_sel = self._find_rows(var="process", val=process, is_bound=is_bound)
        rule_sel = self._find_rows(var="rule", val=rule, is_bound=is_bound)

        sel = role_sel & process_sel & rule_sel

        df = self._data.loc[sel]
        if df.empty:
            msg = f"No data returned with {role=}, {process=}, {rule=}."
            raise UserWarning(msg)
        return df

    def _find_rows(self, var: str, val: str | None, is_bound: bool) -> pd.Series:
        """Find the rows in a columns that match the regex.

        Args:
            var (str): Name of the column.
            val (str | None): Searched string.
            is_bound (bool): True = add the boundaries.

        Returns:
            pd.Series: Boolean series with True when value is found.
        """
        assert var in self._data.columns
        if val:
            val_rgx = rf"\b{val}\b" if is_bound else val
            sel = self._data[var].str.contains(val_rgx, flags=re.IGNORECASE, regex=True)
        else:
            sel = pd.Series(True, index=self._data.index, dtype=bool)
        return sel
