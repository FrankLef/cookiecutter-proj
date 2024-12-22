from pathlib import Path

class PathFinder:
    
    def __init__(self, paths: dict[str, str], base_path: Path):
        if not base_path.is_dir():
            raise NotADirectoryError("{base_path} not found.")
        self._paths = paths
        self._base_path = base_path
        
    def get_path(self, id: str, sub: str | None = None, name: str | None = None) :
        if id in self._paths.keys():
            a_path = self._base_path.joinpath(self._paths[id])
        else:
            raise KeyError(f"'{id}' is an invalid data path id.")
        if sub:
            a_path = a_path.joinpath(sub)
        if not a_path.is_dir():
            raise NotADirectoryError(f"{a_path} is not a directory.")
        if name:
            a_path = a_path.joinpath(name)
        return a_path