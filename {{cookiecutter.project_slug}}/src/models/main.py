import sys
from pathlib import Path

from prefect import flow

# import pyarrow.feather as feather  # noqa

# src path to be able to import the settings
src_path = Path(__file__).parent.parent

# add the project path to be able to access the settings
a_path = str(src_path.parent)
if a_path not in sys.path:
    sys.path.insert(1, a_path)

from config import settings  # noqa
from helpers import richmsg  # noqa

process_msg = settings.message.model


@flow(name="models", log_prints=True)
def run_model() -> bool:
    """Modelization.

    Returns:
        bool: True if completed.
    """
    richmsg.print_msg(text=process_msg, type="process")
    return True


if __name__ == "__main__":
    run_model()
