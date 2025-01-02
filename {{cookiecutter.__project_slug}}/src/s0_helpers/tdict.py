from pathlib import Path
import pandas as pd
import re


class TDict:
    """Table dictionary with tables' specs"""

    _SCHEMA = {
        "path": str,
        "file": str,
        "table": str,
        "raw_name": str,
        "name": str,
        "label": str,
        "dtype": str,
        "activ": bool,
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
        check = sum([x not in data.columns for x in type(self)._SCHEMA.keys()])
        if not check:
            data = data.astype(type(self)._SCHEMA)
            data.reset_index(drop=True, inplace=True)
            self._data = data
        else:
            raise ValueError(f"{check} required columns missing in the data.")

    def get_data(
        self,
        role: str | None = None,
        process: str | None = None,
        rule: str | None = None,
        activ: bool | None = None,
    ) -> pd.DataFrame:
        """Get filtered data from a table dictionary.

        Args:
            role (str | None, optional): Regexp to filter the role. Defaults to None.
            process (str | None, optional): Regexp to filter the process. Defaults to None.
            rule (str | None, optional): Regexp to filter the rule. Defaults to None.
            activ (bool | None, optional): Select the activ flag. Defaults to None.

        Returns:
            pd.DataFrame: Filtered table dictionary.
        """
        assert isinstance(activ, bool | None)
        df = self._data
        if role:
            sel = df.role.str.contains(
                pat=role, flags=re.IGNORECASE, regex=True, na=True
            )
            df = df[sel]

        if process:
            sel = df.process.str.contains(
                pat=process, flags=re.IGNORECASE, regex=True, na=True
            )
            df = df[sel]

        if rule:
            sel = df.rule.str.contains(
                pat=rule, flags=re.IGNORECASE, regex=True, na=True
            )
            df = df[sel]

        if activ is not None:
            df = df.loc[df.activ == activ]

        return df

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
