from pathlib import Path
import pandas as pd
import pandera as pa
import re


class TDict:
    """Table dictionary with tables' specs"""

    _SCHEMA = pa.DataFrameSchema(
        {
            "path": pa.Column(str),
            "file": pa.Column(str),
            "table": pa.Column(str),
            "raw_name": pa.Column(str),
            "name": pa.Column(str),
            "label": pa.Column(str, nullable=True),
            "dtype": pa.Column(str, nullable=True),
            "activ": pa.Column(bool),
            "role": pa.Column(str, nullable=True),
            "process": pa.Column(str, nullable=True),
            "rule": pa.Column(str, nullable=True),
            "desc": pa.Column(str, nullable=True),
            "note": pa.Column(str, nullable=True),
        },
        coerce=True,
        strict=False,
    )

    def __init__(self, data: pd.DataFrame):
        """Table dictionary

        Args:
            data (pd.DataFrame): Dictionary data.
        """
        self._data = data.copy()
        self._SCHEMA.validate(self._data)

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
        if not isinstance(activ, bool | None):
            msg = f"`activ` must be boolean. It is of type '{type(activ)}'."
            raise AssertionError(msg)
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
