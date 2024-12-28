import pandas as pd
import re


class TDict:
    """Table dictionary with tables' specs"""

    def __init__(self, data: pd.DataFrame):
        """Initialize a table dictionary.

        Args:
            path (Path): Path of excel file.

        Raises:
            FileNotFoundError: Excel file is not found.
        """
        """These 3 columns must be of string type which is not the case when
        a column is empty. Otherwise the filter will raise an exception.
        """
        self._data = data.astype({"role": str, "process": str, "rule": str})

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
