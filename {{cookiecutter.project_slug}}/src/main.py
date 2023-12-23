"""The main module manage the functional flow.

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

process_msg = settings.message.main
from helpers import richmsg  # noqa


@flow(name="main", log_prints=True)
def run_main(msg: str, verbose=False) -> bool:
    if not msg:
        msg = process_msg
    richmsg.print_msg(text=process_msg, type="process")
    return True


if __name__ == "__main__":
    run_main(process_msg)
