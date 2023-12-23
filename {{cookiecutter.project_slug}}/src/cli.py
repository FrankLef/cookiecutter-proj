import argparse
import sys
import winsound as ws
from pathlib import Path

import main as main
from helpers import richmsg

# add the project path to be able to access the settings
a_path = str(Path(__file__).parent.parent)
if a_path not in sys.path:
    sys.path.insert(1, a_path)

# import winsound as ws
from config import settings  # noqa

the_starts = tuple(settings.starts)


parser = argparse.ArgumentParser(
    prog="pipeline", description="Run a data pipeline", epilog="Good luck."
)
parser.add_argument(
    "start",
    action="store",
    default=("preproc"),
    choices=the_starts,
    nargs=1,
    help="sets the pipeline's starting point (default: %(default)s)",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="output detailed info to the console.",
)
parser.add_argument(
    "-s",
    "--single",
    action="store_true",
    help="run the command as a single step, not as a pipeline.",
)
args = parser.parse_args()


if __name__ == "__main__":
    verb = args.verbose
    # print(f"{verb=}")
    single = args.single
    # print(f"{single=}")
    start = args.start[0]
    # print(f"{start=}")
    idx = the_starts.index(start)
    starts = the_starts[idx:] if not single else (the_starts[idx],)
    check = [x not in the_starts for x in starts]
    if any(check):
        raise ValueError("There is an invalid start value. Weird.")
    msg = f"Processing pipeline in {(nsteps:=len(starts))} steps: {starts=}"
    richmsg.print_msg(text=msg)
    main.run_pipeline(starts=starts, verbose=verb)
    msg = f"Pipeline in {nsteps} steps completed with success."
    richmsg.print_msg(msg, type="Success")
    ws.MessageBeep(type=ws.MB_ICONASTERISK)
