from pathlib import Path
import pandas as pd
import re


class DDict:
    """Data dictionary with specs by variable."""

    _SCHEMA = {
        "table": str,
        "raw_name": str,
        "name": str,
        "label": str,
        "raw_dtype": str,
        "dtype": str,
        "key": bool,
        "activ": bool,
        "role": str,
        "process": str,
        "rule": str,
        "desc": str,
        "note": str,
    }

    _KEYS = ["table", "name"]

    _SEP = "\u00ac"  # string separator. The not '¬' sign.

    def __init__(self, data: pd.DataFrame | None = None):
        """Data dictionary

        Args:
            data (pd.DataFrame): Data dictionary in a data frame.

        Raises:
            ValueError: Required columns are missing.
        """
        if data is not None:
            msg = f"Input must be a data frame. It is a {type(data)}"
            assert isinstance(data, pd.DataFrame), msg
            self._data = data
            self._validate_data()
            self._data.set_index(keys=self._KEYS, drop=False, inplace=True)
        else:
            self._data = pd.DataFrame(columns=type(self)._SCHEMA.keys()).astype(
                type(self)._SCHEMA
            )

    def _validate_data(self):
        self._validate_columns()
        self._repl_ws()
        self._validate_null(schema=["table", "raw_name", "name"])
        self._validate_uniq()

    def _validate_columns(self):
        self._data.columns = self._data.columns.str.lower()
        check = [x not in self._data.columns for x in type(self)._SCHEMA.keys()]
        err_nb = sum(check)
        if err_nb:
            raise ValueError(f"{err_nb} required columns missing in the data.")
        else:
            self._data = self._data.astype(type(self)._SCHEMA)

    def _repl_ws(self):
        cols = self._data.select_dtypes(include=["object", "string"]).columns
        self._data[cols] = self._data[cols].apply(
            lambda x: x.replace(to_replace=r"^\s*$|^None$", value="", regex=True)
        )

    def _validate_null(self, schema: list[str]):
        for nm in schema:
            err_nb = sum(self._data[nm].isna())
            if err_nb:
                raise ValueError(f"{err_nb} NA values in the '{nm}' column.")

    def _validate_uniq(self):
        raw_name_col = self._data["table"] + self._SEP + self._data["raw_name"]
        name_col = self._data["table"] + self._SEP + self._data["name"]
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
        key: bool | None = None,
        activ: bool | None = None,
        is_bound: bool = True,
    ) -> pd.DataFrame:
        """Get filtered data from a data dictionary.

        Args:
            role (str | None, optional): Name of the role. Defaults to None.
            process (str | None, optional): Name of the porcess. Defaults to None.
            rule (str | None, optional): Name of the rule. Defaults to None.
            key (bool | None, optional): Key flag. Defaults to None.
            activ (bool | None, optional): Activ flag. Defaults to None.
            is_bound (bool, optional): Word boundaries flag. Defaults to True.

        Returns:
            pd.DataFrame: Filtered data frame.
        """
        role_sel = self._find_rows(var="role", val=role, is_bound=is_bound)
        process_sel = self._find_rows(var="process", val=process, is_bound=is_bound)
        rule_sel = self._find_rows(var="rule", val=rule, is_bound=is_bound)

        sel = role_sel & process_sel & rule_sel

        df = self._data.loc[sel]
        if key is not None:
            df = df.loc[df["key"] == key]
        if activ is not None:
            df = df.loc[df["activ"] == activ]

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

    def get_ddict(self, data: pd.DataFrame, table_nm: str) -> pd.DataFrame:
        """Create the data dictionary table describing a data frame.

        Args:
            data (pd.DataFrame): Data frame to process.
            table_nm (str): Name of the table.

        Returns:
            pd.DataFrame: A data dictionary table.
        """
        the_names = [*data.dtypes.index.values]
        the_dtypes = [str(x) for x in data.dtypes]
        specs = pd.DataFrame(
            {
                "table": table_nm,
                "raw_name": the_names,
                "name": the_names,
                "label": pd.NA,
                "raw_dtype": the_dtypes,
                "dtype": the_dtypes,
                "key": False,
                "activ": True,
                "role": pd.NA,
                "process": pd.NA,
                "rule": pd.NA,
                "desc": pd.NA,
                "note": pd.NA,
            },
            index=[*range(len(the_names))],
        )
        specs.set_index(keys=self._KEYS, drop=False, inplace=True)
        return specs

    def update(self, data: pd.DataFrame, table_nm: str):
        """Update the data dictionary object.

        Args:
            data (pd.DataFrame): Data frame to process.
            table_nm (str): Name of the table.
        """
        # get dictionary of source data
        src_ddict = self.get_ddict(data, table_nm=table_nm)

        sel = ~src_ddict.index.isin(self._data.index)
        src_ddict_sel = src_ddict[sel]
        self._data = pd.concat([self._data, src_ddict_sel])
        self._data.set_index(keys=self._KEYS, drop=False, inplace=True)

    def clean(self):
        """Clean the ddict to convert to string,  remove NaN, etc."""
        rgx = re.compile(r"^nan$|^none$", flags=re.IGNORECASE)
        # all object columns should be string in ddict
        cols = self._data.select_dtypes(include="object").columns
        self._data[cols] = self._data[cols].astype("string")
        self._data[cols] = self._data[cols].replace(regex=rgx, value=pd.NA)

    @property
    def path(self):
        """Get path for the DDict file."""
        return self._path

    @path.setter
    def path(self, path: Path) -> Path:
        """Set path for the DDict file."""
        assert isinstance(path, Path), "`path` must be a Path object."
        self._path = path
        return self._path
