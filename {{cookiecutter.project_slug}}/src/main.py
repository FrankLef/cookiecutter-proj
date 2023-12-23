"""The pipeline manages the analytical data flow.

The pipeline will run the script in analytical order from the given step to
the end or just ofr a single step, depending on the user's choice.

The analytical steps are as follows:

1. ETL: Extract, transform and load the raw data.
2. Preprocessing: Preprocessing the data.
3. Feature engineering: Feature engineering.
4. Modelization: Compute the modelization.
5. Winding up: Final clean up, export, etc.
"""
import sys
from pathlib import Path

from prefect import flow

# src path
src_path = Path(__file__).parent

# add the project path to be able to access the settings
a_path = str(src_path.parent)
if a_path not in sys.path:
    sys.path.insert(1, a_path)

from config import settings  # noqa

the_starts = tuple(settings.starts)

a_path = str(src_path.joinpath("etl"))
if a_path not in sys.path:
    sys.path.insert(1, a_path)

from etl.main import run_etl  # noqa
from features.main import run_feat  # noqa
from models.main import run_model  # noqa
from preproc.main import run_preproc  # noqa
from windup.main import run_windup  # noqa


@flow(name="pipeline", log_prints=True)
def run_pipeline(starts: tuple[str, ...], verbose: bool = False) -> int:
    """Process the analytical pipeline.

    Args:
        starts (tuple[str, ...]python main.copy()): id of the analytical steps.
        verbose (bool, optional): If `True` be verbose. Defaults to False.

    Returns:
        int: Return the number of steps processed.
    """
    if the_starts[0] in starts:
        run_etl()
    if the_starts[1] in starts:
        run_preproc()
    if the_starts[2] in starts:
        run_feat()
    if the_starts[3] in starts:
        run_model()
    if the_starts[4] in starts:
        run_windup()
    return len(starts)


if __name__ == "__main__":
    idx = the_starts.index("preproc")
    the_defaults = the_starts[idx:]
    run_pipeline(starts=the_defaults)
