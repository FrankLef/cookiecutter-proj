import pandas as pd
from config import settings

data_path = settings.paths.data
tdict_nm = settings.tdict

def main(subprocess: str) -> int:
    fn = data_path.joinpath(tdict_nm)
    if fn.is_file():
        df = pd.read_excel(fn)
        nrow = len(df.axes[0])
        msg = f"'{tdict_nm}' has {nrow} rows."
        print(msg)
    else:
        msg = f"'{fn}' not found."
        raise FileNotFoundError(msg)
    return 0