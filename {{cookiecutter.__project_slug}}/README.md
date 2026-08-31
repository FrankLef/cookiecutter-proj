# {{cookiecutter.project_name}}

<!-- badges: start -->
[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
<!-- badges: end -->

## Introduction

This is the main *readme* of the {{cookiecutter.project_name}} project.

The sections below cover the `jobrun` command to
run the project modules as a pipeline in a very simple and straightforward way.

## Jobrun

The project is organised with specific directories that can be called in a
command line interface (CLI). The structure of the directories is described
in the [Directory Structure](#directory-structure) section below.

The entry point is in `{{cookiecutter.__project_slug}}\src\__main__.py`.
For help with the commands the usual `--help` option is available.

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src --help
```

## How to use the jobrun

To run the modules in a given directory, for example the *job1_etl* directory,
wou must be in the project directory and use this command

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe etl
```

This will run all the files whose name begins with the prefix **run** in the
*job1_etl* directory in alphabetical order.

To run a specific module in a directory, for example to run *run99a_todo.py* in
the *job1_etl* directory, you can use a regex pattern as follows:

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transf --pat todo
```

## How to use the workflow for a pipeline

Very often, you will probably want to use several directories as in a pipeline.
For example to run the *setup* and *etl* directories you will do

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe setup,etl
```

**The order is unimportant** because the `jobrun` will always run the directories
and their files in alphabetical order.

### How to use the pattern

As mentioned in the above section you can use a regex pattern to run a
specific file. For example

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe etl --pat todo
```

would run any file starting containing *todo* in its name.

If you use `--pat todo` with several directories in a pipeline, the pattern
will be applied to all directories in the pipeline.

### Directories

The *Jobs* are the subdirectories of the `src` directory and are always name
*job*, then any number of characters  or number foloowed by and underscore.
They will processed in alphabetical order. That is with the regex pattern
`^job.+_.+`.

See the [directory structure](#directory-structure) for an example.

### Directory Structure

This is a proposed structure of the project. It can be modified simply by changing
the name of the directories and files.

```text
{{cookiecutter.__project_slug}}
├── .gitignore                <- GitHub's `.gitignore` customized for python.
├── config.py                 <- Script used `dynaconf` to manage settings.
├── pre-commit-config.yaml    <- Settings for `pre-commit`.
├── LICENSE                   <- The project's license.
├── Makefile                  <- Scripts to automate tasks.
├── mkdocs.yaml               <- Settings for `mkdocs`.
├── pyproject.toml            <- Configuration file used by `poetry`.
├── settings.toml             <- Project's settings used by `dynaconf`.
├── .secrets.toml             <- Optional: Secret settings used by `dynaconf`.
├── README.md                 <- The top-level README for developers using this project.
├── data                      <- Data directories used throughout the project.
│   ├── d0_setup              <- Temporary folder. These files can usually be deleted.
│   ├── d1_raw                <- Original, immutable data.
|   ├── d2_transf             <- Data being transformed.
|   ├── d3_ready              <- Transformed data ready to use.
│   ├── d4_preproc            <- Preprocessed data to used for EDA.
│   ├── d5_eda                <- Data used for exploratory data analysis.
│   ├── d9_teard              <- Final data sets. Usually used for reports and graphics.
|   └── ...
├── docs                      <- GitHub pages website.
│   ├── explanation.md        <- Understanding-oriented documentation.
│   ├── how-to-guides.md      <- Problem-oriented documentation.
│   ├── index.md              <- The index page for the whole documentation.
│   ├── reference.md          <- Information-oriented documentation.
│   ├── tutorials.md          <- Learning-oriented documentation.
|   └── ...
├── notes                     <- Notebooks. Naming convention is a prefix,
│   │                            a number (for ordering), and a short `_`
│   │                            delimited description, e.g. `fl_eda_01a_explore_data.ipynb`.
│   ├── tmp_01a.ipynb         <- Notebook example.
│   └── viz                   <- Visualizations such as plots and tables used by notebooks.
├── reports                   <- Reports, usually in markdown or other formats (pdf, html, etc.).
│   ├── data                  <- Data used in reporting.
│   └── viz                   <- Visualizations such as plots and tables used in reporting.
├── src                       <- Store the source code.
│   ├── __init__.py           <- The module's initialize file.
│   ├── __main__.py           <- Main CLI entry point.
│   ├── _registry             <- Values, instantiated classes, shared by all modules.
│   │   ├── registry.py       <- Values shared by all modules. Equivalent to a singleton.
|   |   └── ...
│   ├── job0_setup            <- Directory of job 'setup'.
│   │   ├── __init__.py
|   |   └── ...
|   ├── job1_etl              <- Directory of job 'etl'.
│   │   ├── __init__.py
|   |   └── ...
|   └── ...
└── tests                     <- All test and fixtures files used in testing.
    ├── __init__.py
    ├── fixtures              <- Where to put example inputs and outputs
    │   ├── input.json        <- Test input data.
    │   └── output.json       <- Test output data.
    ├── conftest.py           <- Configurations used by `pytest`.
    ├── test_sample.py        <- Test example to verify `pytest`.
    └── ...
```
