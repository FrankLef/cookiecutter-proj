from pathlib import Path
import pandas as pd

from config import settings

data_path = Path(__file__).parents[2].joinpath("data", settings.tdict)

def main(path: Path = data_path, role_rgx: str = ".", process_rgx: str = ".") -> pd.DataFrame:
    if path.is_file():
        df = pd.read_excel(path)
        nrow = len(df.axes[0])
        msg = f"'{path}' has {nrow} rows."
        print(msg)
    else:
        msg = f"'{path}' not found."
        raise FileNotFoundError(msg)
    df = df[df.role.str.match(role_rgx) & df.process.str.match(process_rgx)]
    if not len(df.axes[0]):
        msg = f"No tdict for {role_rgx=} and {process_rgx=}."
        raise ValueError(msg)
    # print(df.shape)
    return df
