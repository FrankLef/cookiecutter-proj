import pandas as pd


class TDict:
    """Table dictionary with tables' specs"""

    def __init__(self, data: pd.DataFrame):
        """Initialize a table dictionary.

        Args:
            path (Path): Path of excel file.

        Raises:
            FileNotFoundError: Excel file is not found.
        """
        self._data = data

    def get_data(self, role_rgx: str = ".*", process_rgx: str = ".*") -> pd.DataFrame:
        """Get filtered data from a table dictionary.

        Args:
            role_rgx (str, optional): Regex for the role. Defaults to ".*".
            process_rgx (str, optional): Regex for the process. Defaults to ".*".

        Raises:
            ValueError: The filtered specs are empty.

        Returns:
            pd.DataFrame: Filtered data in a data frame.
        """
        sel = self._data.role.str.match(role_rgx) & self._data.process.str.match(
            process_rgx
        )
        df = self._data[sel]
        if df.empty:
            msg = f"No tdict for {role_rgx=} and {process_rgx=}."
            raise ValueError(msg)
        return df
