import argparse
import sys
import winsound as ws
from pathlib import Path

# add the project path to be able to access the settings
src_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.insert(1, src_path)

import main  # noqa

parser = argparse.ArgumentParser(
    prog="main_flow", description="Run a functional flow", epilog="Good luck."
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="output detailed info to the console.",
)
args = parser.parse_args()


if __name__ == "__main__":
    verb = args.verbose
    print(f"{verb=}")
    main.run_main(verbose=verb)
    ws.MessageBeep(type=ws.MB_ICONASTERISK)
