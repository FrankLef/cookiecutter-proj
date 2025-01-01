from pathlib import Path
import pandas as pd
import re

class TDict:
    """Table dictionary with tables' specs"""

    _SCHEMA = {
        "path": str,
        "file": str,
        "table": str,
        "name": str,
        "raw_name": str,
        "label": str,
        "dtype": str,
        "role": str,
        "process": str,
        "rule": str,
        "desc": str,
        "note": str,
    }

    def __init__(self, data: pd.DataFrame):
        """Data dictionary

        Args:
            data (pd.DataFrame): Data dictionary in a data frame.

        Raises:
            ValueError: Required columns are missing.
        """
        data.columns = data.columns.str.lower()  # must be in lower case
        check = sum([x not in data.columns for x in self._SCHEMA.keys()])
        if not check:
            data = data.astype(self._SCHEMA)
            data.reset_index(drop=True, inplace=True)
            self._data = data
        else:
            raise ValueError(f"{check} required columns missing in the data.")

    def get_data(
        self,
        role: str | None = None,
        process: str | None = None,
        rule: str | None = None,
        is_bound: bool = True,
    ) -> pd.DataFrame:
        """Get filtered data from a table dictionary.

        Args:
            role (str | None, optional): Regex for the role. Defaults to None.
            process (str | None, optional): Regex for the process. Defaults to None.
            rule (str | None, optional): Regex for the rule. Defaults to None.
            is_bound (bool, optional): Add regex boundaries. Defaults to True.

        Returns:
            pd.DataFrame: Filtered data in a data frame.
        """
        role_sel = self._find_rows(var="role", val=role, is_bound=is_bound)
        process_sel = self._find_rows(var="process", val=process, is_bound=is_bound)
        rule_sel = self._find_rows(var="rule", val=rule, is_bound=is_bound)

        sel = role_sel & process_sel & rule_sel

        df = self._data.loc[sel]
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
    
    @property
    def path(self):
        """Get path for the TDict file."""
        return self._path
    
    @path.setter
    def path(self, path: Path) -> Path:
        """Set path for the TDict file."""
        assert isinstance(path, Path), "`path` must be a Path object."
        self._path = path
        return self._path
