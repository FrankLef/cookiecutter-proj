from pathlib import Path
import pandas as pd

class TDict:
    def __init__(self, path: Path):
        if not path.is_file():
            raise FileNotFoundError(f"{path} not found.")
        self._path = path
        self._specs = pd.read_excel(path)
        
    def get_specs(self, role_rgx: str = ".", process_rgx: str = "."):
        sel = self._specs.role.str.match(role_rgx) & self._specs.process.str.match(process_rgx)
        df = self._specs[sel]
        if df.empty:
            msg = f"No tdict for {role_rgx=} and {process_rgx=}."
            raise ValueError(msg)
        return df