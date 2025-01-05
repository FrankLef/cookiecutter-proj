from pathlib import Path
import pandas as pd
import pandera as pa
import re


class DDict:
    """Data dictionary with specs by variable."""

    _KEYS = ["table", "name"]

    _SCHEMA = pa.DataFrameSchema(
        {
            "table": pa.Column(str),
            "raw_name": pa.Column(str),
            "name": pa.Column(str),
            "label": pa.Column(str, nullable=True, default=pd.NA),
            "raw_dtype": pa.Column(str, nullable=True, default=pd.NA),
            "dtype": pa.Column(str, nullable=True, default=pd.NA),
            "activ": pa.Column(bool, default=True),
            "key": pa.Column(bool, default=False),
            "null_ok": pa.Column(bool, default=True),
            "role": pa.Column(str, nullable=True, default=pd.NA),
            "process": pa.Column(str, nullable=True, default=pd.NA),
            "rule": pa.Column(str, nullable=True, default=pd.NA),
            "desc": pa.Column(str, nullable=True, default=pd.NA),
            "note": pa.Column(str, nullable=True, default=pd.NA),
        },
        unique=_KEYS,
        coerce=True,
        strict=True,
    )

    def __init__(self, data: pd.DataFrame | None = None):
        """Data dictionary

        Args:
            data (pd.DataFrame): Data dictionary in a data frame.

        Raises:
            ValueError: Required columns are missing.
        """
        if data is not None:
            self._data = data.copy()
            self._SCHEMA.validate(self._data)
            self._data.set_index(keys=type(self)._KEYS, inplace=True)
        else:
            dt = {key: str(val) for key, val in self._SCHEMA.dtypes.items()}
            self._data = pd.DataFrame(columns=dt.keys()).astype(dt)

    def get_data(
        self,
        table: str | None = None,
        role: str | None = None,
        process: str | None = None,
        rule: str | None = None,
        activ: bool | None = None,
        key: bool | None = None,
    ) -> pd.DataFrame:
        """Get filtered data from a data dictionary.

        Args:
            table (str | None, optional): Regexp to filter the table. Defaults to None.
            role (str | None, optional): Regexp to filter the role. Defaults to None.
            process (str | None, optional): Regexp to filter the process. Defaults to None.
            rule (str | None, optional): Regexp to filter the rule. Defaults to None.
            activ (bool | None, optional): Select the activ flag. Defaults to None.
            key (bool | None, optional): Select the key flag. Defaults to None.

        Returns:
            pd.DataFrame: Filtered data dictionary.
        """
        if not isinstance(activ, bool | None):
            raise TypeError(f"'{activ}' has invalid type '{type(activ)}'.")
        if not isinstance(key, bool | None):
            raise TypeError(f"'{key}' has invalid type '{type(key)}'.")
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

        if activ is not None:
            df = df.loc[df.activ == activ]

        if key is not None:
            df = df.loc[df.key == key]

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

        n = len(the_names)

        dt = {key: str(val) for key, val in self._SCHEMA.dtypes.items()}
        df = pd.DataFrame(columns=dt.keys()).astype(dt)
        df.table = [table_nm] * n
        df.raw_name = the_names
        df.name = the_names
        df.label = pd.NA
        df.raw_dtype = the_dtypes
        df.dtype = the_dtypes
        df.activ = True
        df.key = False
        df.null_ok = True
        df.role = pd.NA
        df.process = pd.NA
        df.rule = pd.NA
        df.desc = pd.NA
        df.note = pd.NA

        self._SCHEMA.validate(df)

        df.set_index(keys=type(self)._KEYS, inplace=True)
        return df

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
        err_if = self._data.key & self._data.null_ok
        err_nb = sum(err_if)
        if err_nb:
            raise AssertionError(f"{err_nb} keys have 'null_ok' set to True.")

    def get_schema(self, table: str, coerce=True, strict=False):
        """Get a DataFrameSchema object from the data dictionary."""
        tbl = self.get_data(table=table)
        if tbl.empty:
            raise ValueError(f"'{tbl}' is empty.")
        tbl.reset_index(inplace=True)
        the_cols = {}
        the_keys = []
        for row in tbl.itertuples():
            if row.activ:
                the_cols[row.name] = pa.Column(
                    name=row.name,
                    dtype=row.dtype,
                    nullable=row.null_ok,
                    title=row.label,
                    description=row.desc,
                )
                if row.key:
                    the_keys.append(row.name)

        the_keys = None if not the_keys else the_keys  # type: ignore

        schema = pa.DataFrameSchema(
            columns=the_cols, coerce=coerce, strict=strict, unique=the_keys
        )

        return schema

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
