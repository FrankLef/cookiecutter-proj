from typing import NamedTuple, Final
from pathlib import Path
import re
import json
from rich import print as rprint
from importlib import import_module
import winsound


class DirSpecs(NamedTuple):
    """The directory specifications."""

    priority: int
    name: str
    label: str
    prefix: str
    dir: str
    emo: str
    song: str


class WorkFlow:
    """The workflow to run the modules."""

    def __init__(self, root_path: Path | None = None, dirs_file: Path | None = None):
        self._all_specs: dict[str, DirSpecs] = {}
        self._root_path = self.check_root_path(root_path)
        self._dirs_file = self.check_dirs_file(dirs_file)

    @property
    def root_path(self) -> Path:
        """The root_path path is where all workflow paths are located."""
        return self._root_path

    @property
    def dirs_file(self) -> Path:
        """The full path to the workflow.json file."""
        return self._dirs_file

    @property
    def names(self):
        """The name (key) of all the workflow directories."""
        return self._all_specs.keys()

    def add(self, specs: DirSpecs):
        """Add a directory specifications to the overall dictionnary."""
        self._all_specs[specs.name] = specs

    def get(self, name: str):
        """Get a directory specifications from the overall dictionnary."""
        return self._all_specs[name]

    def check_root_path(self, root_path: Path | None = None) -> Path:
        """Validate the root_path."""
        if not root_path:
            a_path: Path = Path(__file__).parents[1]
        else:
            a_path = root_path

        if not a_path.is_dir():
            raise NotADirectoryError(f"Invalid root directory:\n{a_path}")

        return a_path

    def check_dirs_file(self, dirs_file: Path | None = None) -> Path:
        """Validate the path to the workflow.json file."""
        DIRS_FILE: Final[str] = "workflow.json"  # the default dirs file

        if not dirs_file:
            a_file: Path = Path(__file__).parent.joinpath(DIRS_FILE)
        else:
            a_file = dirs_file

        if not a_file.is_file():
            raise FileNotFoundError(f"Invalid dirs file:\n{a_file}")

        return a_file

    def execute(self, jobs_args: str, pat: str | None) -> None:
        """This execute the different steps of the program."""
        self.load()
        self._pat = pat
        self.parse_jobs(jobs_args)
        self.sequence_jobs()
        self.run_jobs()
        # WAV_FILE:Final[str]= "achievement-bell-600.wav"
        # sound_file: Path = Path(__file__).parent.joinpath(WAV_FILE)
        # winsound.PlaySound(str(sound_file), flags=winsound.SND_FILENAME)
        # winsound.MessageBeep(winsound.MB_ICONASTERISK)
        winsound.Beep(440, 500)
        
    def load(self):
        """Load all directory specifications from the json file."""
        dirs_file = self._dirs_file
        try:
            with open(dirs_file, mode="r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            msg = f"File not found. This was checked when initializing. Weird.\n {dirs_file}"
            print(msg)
        except json.JSONDecodeError:
            print(f"Invalid JSON format in\n'{dirs_file}'.")
        for dir in data:
            specs = DirSpecs(**dir)  # type: ignore
            self.add(specs)

        # NOTE: Must sort the dictionnary by priority.
        sorted_specs = sorted(
            self._all_specs.items(), key=lambda item: item[1].priority
        )
        sorted_dict_specs = dict(sorted_specs)
        self._all_specs = sorted_dict_specs

    def parse_jobs(self, jobs_args: str) -> None:
        """Parse the jobs from the CLI."""
        # remove all whitspace, tab, newline, etc
        jobs = re.sub(r"\s+", "", jobs_args)
        if not jobs:
            msg: str = f"The job arguments '{jobs_args}' is invalid."
            raise ValueError(msg)
        jobs_clean = jobs.lower().split(sep=",")
        jobs_clean = [x[:2] for x in jobs_clean]
        jobs_todo = set(jobs_clean)
        if not len(jobs_todo):
            msg = f"No jobs obtained from '{jobs_args}'."
            raise AssertionError(msg)
        self._jobs_todo = jobs_todo

    def sequence_jobs(self) -> None:
        """Sequence the jobs according to the establieshed priorities."""
        jobs_todo = self._jobs_todo
        jobs_names = list(self.names)
        try:
            # NOTE: We can use index because the dictionary is sorted by priority in the load function above.
            jobs_pos = sorted([jobs_names.index(x) for x in jobs_todo])
        except ValueError:
            msg: str = "A job is not in the list of available jobs."
            raise ValueError(msg)
        if not jobs_pos:
            raise ValueError("No job found in the list of available jobs.")
        jobs_sequence = [jobs_names[pos] for pos in jobs_pos]
        self._jobs_sequence = jobs_sequence

    def get_full_pattern(self, specs: DirSpecs, pat: str | None) -> str:
        """Create the regex pattern used to filter the files."""
        prefix = specs.prefix
        if pat is None:
            full_pat = "^" + prefix + r".+_.*" + "[.]py$"
        else:
            full_pat = "^" + prefix + r".+_" + pat + "[.]py$"
        return full_pat

    def get_files(self, root_path: Path, specs: DirSpecs, pat: str | None) -> list[str]:
        """Get the list of files in the folder, given a name pattern."""
        full_pattern: str = self.get_full_pattern(specs=specs, pat=pat)

        wd = root_path.joinpath(specs.dir)
        if wd.exists():
            files = [item for item in wd.iterdir() if item.is_file()]
        else:
            raise NotADirectoryError(f"Invalid path\n{wd}")
        the_files = sorted(
            [
                fn.stem
                for fn in files
                if re.match(full_pattern, fn.name, flags=re.IGNORECASE)
            ]
        )
        if not len(the_files):
            msg: str = f"""
            No module found:
            path: {wd}
            pattern: {full_pattern}
            """
            raise ValueError(msg)
        return the_files

    def run_jobs(self) -> None:
        """Run each job required by the user."""
        root_path = self._root_path
        pat = self._pat

        jobs_sequence = self._jobs_sequence
        for job in jobs_sequence:
            specs = self.get(job)
            self.print_run(dir=specs.dir, pat=pat, emo=specs.emo)
            the_files: list[str] = self.get_files(
                root_path=root_path, specs=specs, pat=pat
            )
            self.run_modul(job_dir=specs.dir, files=the_files)

    def run_modul(self, job_dir: str, files: list[str]) -> None:
        """Process the modules in the workflow directory with given pattern."""
        for a_file in files:
            modul = import_module(name="." + a_file, package=job_dir)
            self.print_process(modul_nm=modul.__name__, modul_doc=modul.__doc__)
            try:
                modul.main()
            except NotImplementedError as e:
                if str(e).lower().startswith("skip"):
                    self.print_skip(modul.__name__)
                else:
                    raise
            self.print_complete(modul.__name__)

    def print_run(self, dir: str, pat: str | None, emo: str) -> str:
        """Print the run message."""
        text: str = f"\n:{emo}: Running the modules in [orchid]{dir}[/orchid]"
        if pat:
            text = text + f" with pattern [orchid]{pat}[/orchid]"
        msg = f"[cyan]{text}[/cyan]"
        rprint(msg)
        return msg

    def print_process(self, modul_nm: str, modul_doc: str | None) -> str:
        """Print the process message."""
        text = f"[cyan]Processing [orchid]{modul_nm}[/orchid][/cyan]"
        # msg = f"[cyan]\u21BB  {text}[/cyan]"
        msg = f":arrows_counterclockwise: {text}"

        rprint(msg)
        if modul_doc is not None:
            doc_msg = f"\u2139  {modul_doc}"
            rprint(doc_msg)
        return msg

    def print_skip(self, modul_nm: str) -> str:
        """Print the skip message."""
        msg = f"\u26a0[yellow]  Skip [orchid]{modul_nm}[/orchid][/yellow]"
        rprint(msg)
        return msg

    def print_complete(self, modul_nm: str) -> str:
        """Print the complete message."""
        text = f"Completed [orchid]{modul_nm}[/orchid]\n"
        msg = f"[green]\u2705 {text}[/green]"
        rprint(msg)
        return msg
