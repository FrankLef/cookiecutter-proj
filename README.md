# cookiecutter-proj

<!-- badges: start -->
[![Lifecycle:
stable](https://img.shields.io/badge/lifecycle-stable-brightgreen)](https://lifecycle.r-lib.org/articles/stages)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-^3.10-blue)](https://www.python.org/downloads/release/python-3106/)
[![cookiecutter](https://img.shields.io/badge/cookiecutter-2.1.1-blueviolet)](https://cookiecutter.readthedocs.io/en/stable/)
[![Poetry](https://img.shields.io/badge/poetry-^1.7.1-purple)](https://pypi.org/project/poetry/)
[![Ruff](https://img.shields.io/badge/ruff-^0.2.2-maroon)](https://docs.astral.sh/ruff/)
[![Pre-commit](https://img.shields.io/badge/precommit-^3.5.0-orange)](https://pypi.org/project/pre-commit/)
<!-- badges: end -->

Cookiecutter for simple projects using the most up-to-date setup possible.
Heavily inspired by [Hypermodern-cookiecutter], [cookiecutter-modern-datascience] and
[data-science-template] to whom we are very grateful.

The workflow is organized with this [directory structure](#directory-structure).

## Quickstart

`Makefile` is used repeatedly hereinafter to automate many of
the tasks. It is automatically configured by the cookiecutter to include, the
repo name, project name, etc.

### Step 1 Setup the project structure with `cookiecutter`

Change to the parent location where you want the project to be created.
For example if your project is called `flproj_todo` in the `parent` folder,
then move to `parent` first

    cd ..\parent

verify that `cookiecutter` is properly installed by calling its version

    cookiecutter --version

then generate the project

    cookiecutter https://github.com/FrankLef/cookiecutter-proj.git

and make the new folder the working directory.

    cd ..\parent\flproj_todo

### Step 2 Manage the dependencies with `poetry`

Don't forget to consult the [help poetry](#help-poetry) section in case of
problem of for more details.

Make sure the poetry version used is at least 1.7.

    poetry --version.

Run `poetry shell` to open the poetry shell and avoid using `poetry run` with
all commands

    poetry shell

Run the `make` command `poetry_update`.

    make poetry_update

### Step 3 Setup the new `.git`

#### Create repo in `github`

First create the new repo in github

* **Give the repo the exact same name as the project**. That is keep the
underscore in the name when there one. i.e. `flproj_todo` is also `flproj_todo`
in github.
* Don't create `README`, `.gitignore` and `LICENSE`. They will be created by
the cookiecutter.

#### Initialize the repo

Then initialize git using

    make git_init

### Step 4 Install `pre-commit`

See the [help pre-commit](help-pre-commit-update) for details.

Setup and update `pre-commit`

    make precommit

It is also a good idea to run the hooks against all files to verify them.

    make precommit_run

### Step 5 Verify the features

#### Create the documentation with `mkdocs`

You can also verify that the documentation setup is working by building
the site.

    mkdocs serve

This will give you and output like this

    INFO    -  Building documentation...
    INFO    -  Cleaning site directory
    INFO    -  Documentation built in 0.11 seconds
    INFO    -  [09:26:11] Watching paths for changes: 'docs', 'mkdocs.yaml'
    INFO    -  [09:26:11] Serving on http://127.0.0.1:8000/
    INFO    -  [09:26:31] Browser connected: http://127.0.0.1:8000/

you can see the resulting documentation by ctrl-click on `http://127.0.0.1:8000/`

and when you are done, you can exit the result with

    ctrl^C

#### Code testing with `pytest`

Finally you can verify that `pytest` is working as expected. Use
this command wich runs the tests from the `tests` directory.

    pytest

### Step 6 (optional) Add the ignored directories

Some directories, such as the `\data`, are included in `.gitignore` and
therefore ignored by the cookicutter. You can run `make` to add these extra
directories.

    make ignored_dir

## Help notes

This section gives more details for reference and also to help solve problems
that were encountered and might happen again.

You can also read the `pyproject.toml` provided by this cookiecutter to see
information on the required changes.

### Help poetry

#### Help `poetry_update`

Run the `make` command `poetry_update` so that the following `poetry` command
will run

1. `poetry update`: The `poetry.lock` file will be created and the virtual
environment updated with the right packages and versions
2. `poetry show`: To verify if there are inconsistencies

#### Help poetry environment

Sometimes, especially when reusing a folder that had been used as a project
before, the old environment is still used. To see the environment curently
opened by `poetry` use this

    poetry env list

To delete the old environment use this command

    poetry env remove <python>

### Help pre-commit

#### Help pre-commit update

Once `.git` is setup, make sure to include the pre-commit script in `.git`
by running `pre-commit install` from the poetry shell. Also `pre-commit update`
ensures that the `ruff` is up-to-date. Sometimes warnings
appear about the 'rev' field being mutable, using `pre-commit update`
usually resolves this.

#### Help pre-commit run

No need to run the linter and code formatter separately. Better yet,
you can run all the pre-commit hooks using this useful command

    pre-commit run --all-files

wich is encoded in the MakeFile with the command

    make precommit_run

### `pyarrow`

Use `pyarrow.feather` instead of `feather-format`, `feather.format` exists only
for backward compatibility. `pyarrow` should be installed with
`pip3 install pyarrow` in the local python. Don't install `pyarrow` with
`poetry add pyarrow` or you will get a whole lot of cryptic errors.

## Libraries Used

The primary libraries used are described in sections as follows:

* Template and environment
* Code quality
* Documentation
* Project libraries

### Template and Environment

|Library|Description|
|:-----|:-----------------|
|[cookiecutter]|Project templates|
|[poetry]|Project dependency|

### Code quality

|Library|Description|
|:-----|:-----------------|
|[ruff]|Fast (very) Python linter and code formatter, written in Rust.|
|[pre-commit]|Manage pre-commit hooks|
|[pre-commit-hooks]|Some out-of-the-box hooks for `pre-commit`|
|[pytest]|Framework for testing|
|[mypy]|Static type checker|
|[typeguard]|Type checking for functions|

### Documentation

|Library|Description|
|:-----|:-----------------|
|[MkDocs]|Project documentation|
|[mkdocstrings]|Automatic documentation|
|[mkdocstrings-python]|Automatic documentation|

### Project Libraries

|Library|Description|
|:-----|:-----------------|
|[rich]|Writing rich text to the terminal and display advanced content|
|[typer]|Typer, build great CLIs|
|[dynaconf]|Settings management|
|[tomli]|A lil' TOML parser|
|[requests]|HTTP library for Python|
|[pandas]|Data analysis and manipulation tool|
|[numpy]|Scientific computing|
|[pyodbc]|Access ODBC database|
|[SQLAlchemy]|SQL toolkit and object relational mapper|

## Directory structure

This is how the folders will be organized.

    ├── .gitignore                <- GitHub's Python `.gitignore` customized for this project.
    ├── config.py                 <- Script used `dynaconf` to manage settings.
    ├── pre-commit-config.yaml    <- Settings for `pre-commit`.
    ├── LICENSE                   <- The project's license.
    ├── Makefile                  <- Scripts to automate tasks.
    ├── mkdocs.yaml               <- Settings for `mkdocs`.
    ├── pyproject.toml            <- Configuration file used by `poetry`.
    ├── settings.toml             <- Project's settings used by `dynaconf`.
    ├── .secrets.toml             <- Secret settings used by `dynaconf`.
    ├── README.md                 <- The top-level README for developers using this project.
    ├── data                      <- Data directories used throughout the project.
    │   ├── raw                   <- Original, immutable data.
    |   ├── transf                <- Data being processed and transformed
    |   ├── ready                 <- Transformed, complete data ready to use.
    │   ├── temp                  <- Temporary folder. These files can be deleted.
    |   └── ...
    ├── docs                      <- GitHub pages website.
    │   ├── explanation.md        <- Understanding-oriented documentation.
    │   ├── how-to-guides.md      <- Problem-oriented documentation.
    │   ├── index.md              <- The index page for the whole documentation.
    │   ├── reference.md          <- Information-oriented documentation.
    │   ├── tutorials.md          <- Learning-oriented documentation.
    |   └── ...
    ├── notebooks                 <- Jupyter notebooks. Naming convention is a number (for ordering),
    │   │                            the creator's initials, and a short `_` delimited description, e.g.
    │   │                            `01_fl_exploratory_data_analysis.ipynb`.
    │   ├── data                  <- Data used by notebooks.
    │   └── viz                   <- Visualizations such as plots and tables used by notebooks.
    ├── reports                   <- Reports, usually in markdown or other formats (pdf, html, etc.).
    │   ├── data                  <- Data used in reporting.
    │   └── viz                   <- Visualizations such as plots, figures and tables used in reporting.
    ├── src                       <- Store the source code.
    │   ├── cli.py                <- The main CLI entry point.
    │   ├── helpers               <- Utilities and helper codes.
    │   │   ├── __init__.py
    |   |   └── ...
    |   ├── etl                   <- Code to extract, transform and load the raw data.
    │   │   ├── __init__.py
    |   |   └── ...
    |   └── ...
    └── tests                     <- All test and fixtures files used in testing.
        ├── __init__.py
        ├── fixtures              <- Where to put example inputs and outputs.
        │   ├── input.json        <- Test input data.
        │   └── output.json       <- Test output data.
        ├── test_extract_acc.py   <- Test example on `etl.py`.
        ├── test_samples.py       <- Test example to verify `pytest`.
        └── ...

[cookiecutter]: https://github.com/audreyr/cookiecutter
[Hypermodern-cookiecutter]: https://cookiecutter-hypermodern-python.readthedocs.io/en
[cookiecutter-modern-datascience]: https://github.com/crmne/cookiecutter-modern-datascience
[data-science-template]: https://github.com/khuyentran1401/data-science-template
[poetry]: https://pypi.org/project/poetry/
[ruff]: https://docs.astral.sh/ruff/
[pre-commit]: https://pypi.org/project/pre-commit/
[pre-commit-hooks]: https://github.com/pre-commit/pre-commit-hooks
[pytest]: https://pypi.org/project/pytest/
[mypy]: http://www.mypy-lang.org
[typeguard]: https://typeguard.readthedocs.io/en/latest/
[MkDocs]: https://www.mkdocs.org
[mkdocstrings]: https://mkdocstrings.github.io
[mkdocstrings-python]: https://mkdocstrings.github.io/python/
[dynaconf]: https://www.dynaconf.com
[rich]: https://rich.readthedocs.io/en/stable/introduction.html
[typer]: https://typer.tiangolo.com
[tomli]: https://pypi.org/project/tomli/
[requests]: https://requests.readthedocs.io/en/latest/
[pandas]: https://pandas.pydata.org
[numpy]: https://numpy.org
[pyodbc]: https://pypi.org/project/pyodbc/
[SQLAlchemy]: https://www.sqlalchemy.org
