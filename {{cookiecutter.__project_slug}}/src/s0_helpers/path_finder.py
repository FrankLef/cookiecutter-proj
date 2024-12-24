from pathlib import Path


class PathFinder:
    """Tools to retrieve path from a dictionary of paths."""

    def __init__(self, paths: dict[str, str], base_path: Path):
        """Create a path finder with a dictionary and a base path.

        Args:
            paths (dict[str, str]): Dictionary of paths.
            base_path (Path): Base path of the paths in `paths`.

        Raises:
            NotADirectoryError: The output path is not a valid directory.
        """
        if not base_path.is_dir():
            raise NotADirectoryError("{base_path} not found.")
        self._paths = paths
        self._base_path = base_path

    def get_path(self, id: str, *sub: str, name: str | None = None):
        """_summary_

        Args:
            id (str): The path's key in the path dictionary.
            name (str | None, optional): Name of the file to add to the path. Defaults to None. Defaults to None.

        Raises:
            KeyError: The `id` is not found in the path dictionary.
            NotADirectoryError: The output path is invalid.

        Returns:
            _type_: A complete path.
        """
        if id in self._paths.keys():
            a_path = self._base_path.joinpath(self._paths[id])
            a_path = a_path.joinpath(*sub)
        else:
            raise KeyError(f"'{id}' is an invalid data path id.")
        if not a_path.is_dir():
            raise NotADirectoryError(f"{a_path} is not a directory.")
        if name:
            a_path = a_path.joinpath(name)
        return a_path
