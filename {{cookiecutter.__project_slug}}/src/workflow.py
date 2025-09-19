from dataclasses import dataclass
from typing import Iterable, Final
from pathlib import Path
import re
import json
from rich import print as rprint
from importlib import import_module


@dataclass
class DirSpecs:
    name: str
    label: str
    suffix: str
    dir: str
    emo: str
    song: str

    def get_full_pattern(self, pat: str | None) -> str:
        """Create the regex pattern used to filter the files."""
        suffix = self.suffix
        if pat is None:
            full_pat = "^" + suffix + r".+_.*" + "[.]py$"
        else:
            full_pat = "^" + suffix + r".+_" + pat + "[.]py$"
        return full_pat

    def get_files(self, root_path: Path, pat: str | None) -> list[str]:
        """Get the list of files in the folder, given a name pattern."""
        jobs_dir = self.dir
        full_pattern: str = self.get_full_pattern(pat=pat)

        wd = root_path.joinpath(jobs_dir)
        if wd.exists():
            files = [item for item in wd.iterdir() if item.is_file()]
        else:
            raise NotADirectoryError(f"Invalid path\n{wd}")
        the_files = sorted([fn.stem for fn in files if re.match(full_pattern, fn.name, flags=re.IGNORECASE)])
        if not len(the_files):
            msg: str = f"""
            No module found:
            path: {wd}
            pattern: {full_pattern}
            """
            raise ValueError(msg)
        return the_files


class WorkFlow:
    def __init__(self, root_path: Path | None = None, dirs_file: Path | None = None):
        self._all_specs: dict[str, DirSpecs] = {}
        self._root_path = self.check_root_path(root_path)
        self._dirs_file = self.check_dirs_file(dirs_file)

    @property
    def root_path(self) -> Path:
        return self._root_path

    @property
    def dirs_file(self) -> Path:
        return self._dirs_file

    @property
    def names(self):
        return self._all_specs.keys()

    def check_root_path(self, root_path: Path | None = None) -> Path:
        if not root_path:
            a_path: Path = Path(__file__).parent
        else:
            a_path = root_path

        if not a_path.is_dir():
            raise NotADirectoryError(f"Invalid root directory:\n{a_path}")

        return a_path

    def check_dirs_file(self, dirs_file: Path | None = None) -> Path:
        DIRS_FILE: Final[str] = "workflow.json"  # the default dirs file

        if not dirs_file:
            a_file: Path = Path(__file__).parent.joinpath(DIRS_FILE)
        else:
            a_file = dirs_file

        if not a_file.is_file():
            raise FileNotFoundError(f"Invalid dirs file:\n{a_file}")

        return a_file

    def add(self, dir_specs: DirSpecs):
        self._all_specs[dir_specs.name] = dir_specs

    def get(self, name: str) -> DirSpecs:
        specs = self._all_specs[name]
        return specs

    def fetch(self, names: Iterable[str]):
        specs = [self.get(name) for name in names]
        return specs

    def load(self):
        dirs_file = self._dirs_file
        try:
            with open(dirs_file, mode="r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            msg = f"File not found. This was checked when initializing. Weird.\n {dirs_file}"
            print(msg)
        except json.JSONDecodeError:
            print(f"Invalid JSON format in\n'{dirs_file}'.")
        dirs = data
        for dir in dirs:
            specs = DirSpecs(**dir)  # type: ignore
            self.add(specs)

    def execute(self, jobs_args: str, pat: str | None) -> None:
        self.load()
        self._pat = pat
        self.parse_jobs(jobs_args)
        self.sequence_jobs()
        self.run_jobs()

    def parse_jobs(self, jobs_args: str) -> None:
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
        jobs_todo = self._jobs_todo
        jobs_names = list(self.names)
        try:
            jobs_pos = sorted([jobs_names.index(x) for x in jobs_todo])
        except ValueError:
            msg: str = "A job is not in the list of available jobs."
            raise ValueError(msg)
        if not jobs_pos:
            raise ValueError("No job found in the list of available jobs.")
        jobs_sequence = [jobs_names[pos] for pos in jobs_pos]
        self._jobs_sequence = jobs_sequence

    def run_jobs(self) -> None:
        root_path = self._root_path
        pat = self._pat
        jobs_sequence = self._jobs_sequence
        for job in jobs_sequence:
            specs = self.get(job)
            self.print_run(label=specs.label, emo=specs.emo)
            the_files: list[str] = specs.get_files(root_path=root_path, pat=pat)
            self.run_modul(job_dir=specs.dir, files=the_files)

    def run_modul(self, job_dir: str, files: list[str]) -> None:
        """Process the modules in the src directory with given pattern."""
        for a_file in files:
            modul = import_module(name="." + a_file, package=job_dir)
            self.print_process(modul.__name__)
            modul.main()
            self.print_complete(modul.__name__)

    def print_run(self, label: str, emo: str) -> str:
        text = f"Run the {label} modules. :{emo}:"
        msg = f"[gold3]\u2022 {text}[/gold3]"
        rprint(msg)
        return msg

    def print_process(self, modul_nm: str) -> str:
        text = f"Processing [orchid]{modul_nm}[/orchid]\u2026"
        msg = f"[gold3]\u2022 {text}[/gold3]"
        rprint(msg)
        return msg

    def print_complete(self, modul_nm: str) -> str:
        text = f"Completed [orchid]{modul_nm}[/orchid]"
        msg = f"[green]\u2713 {text}[/green]"
        rprint(msg)
        return msg
