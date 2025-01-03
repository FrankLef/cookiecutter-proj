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
            self._data.set_index(keys=type(self)._KEYS, inplace=True)
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
            lambda x: x.replace(to_replace=r"^\s*$|^None$", value=pd.NA, regex=True)
        )

    def _validate_null(self, schema: list[str]):
        for nm in schema:
            err_nb = sum(self._data[nm].isna())
            if err_nb:
                raise ValueError(f"{err_nb} NA values in the '{nm}' column.")

    def _validate_uniq(self):
        raw_name_col = self._data["table"] + type(self)._SEP + self._data["raw_name"]
        name_col = self._data["table"] + type(self)._SEP + self._data["name"]
        raw_name_nb = raw_name_col.duplicated().sum()
        name_nb = name_col.duplicated().sum()
        if raw_name_nb | name_nb:
            msg = f"There are {raw_name_nb} duplicated values in 'raw_name' and {name_nb} values in 'name'."
            raise ValueError(msg)

    def get_data(
        self,
        table: str | None = None,
        role: str | None = None,
        process: str | None = None,
        rule: str | None = None,
        key: bool | None = None,
        activ: bool | None = None,
    ) -> pd.DataFrame:
        """Get filtered data from a data dictionary.

        Args:
            table (str | None, optional): Regexp to filter the table. Defaults to None.
            role (str | None, optional): Regexp to filter the role. Defaults to None.
            process (str | None, optional): Regexp to filter the process. Defaults to None.
            rule (str | None, optional): Regexp to filter the rule. Defaults to None.
            key (bool | None, optional): Select the key flag. Defaults to None.
            activ (bool | None, optional): Select the activ flag. Defaults to None.

        Returns:
            pd.DataFrame: Filtered data dictionary.
        """
        assert isinstance(activ, bool | None)
        assert isinstance(key, bool | None)
        df = self._data
        if table:
            sel = df.index.get_level_values("table").str.contains(
                pat=table, flags=re.IGNORECASE, regex=True, na=True
            )
            df = df[sel]

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

        if key is not None:
            df = df.loc[df.key == key]
        if activ is not None:
            df = df.loc[df.activ == activ]

        return df

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
        specs.set_index(keys=type(self)._KEYS, inplace=True)
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
        # Important: Must concatenate first to avoid index problem when
        # self._data is empty.
        self._data = pd.concat([src_ddict_sel, self._data])

    def clean(self):
        """Clean the ddict to convert to string,  remove NaN, etc."""
        rgx = re.compile(r"^\s*$|^nan$|^none$", flags=re.IGNORECASE)
        # all object columns should be string in ddict
        cols = self._data.select_dtypes(include="object").columns
        self._data[cols] = self._data[cols].astype("string")
        self._data[cols] = self._data[cols].replace(regex=rgx, value=pd.NA)

    def audit(self):
        """Check for logical error in the data dictionary."""
        err_if = self._data.key & ~self._data.activ
        err_nb = sum(err_if)
        if err_nb:
            raise AssertionError(f"{err_nb} keys have 'activ' set to False.")

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
