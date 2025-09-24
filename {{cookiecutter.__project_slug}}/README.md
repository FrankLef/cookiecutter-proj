# {{cookiecutter.project_name}}

<!-- badges: start -->
[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
<!-- badges: end -->

## Introduction

This is the main *readme* of the {{cookiecutter.project_name}} project.

The sections below cover the `workflow` which is the command line interface to
run the project modules as a pipeline in avery simple and straightforward way.

## Workflow

The project is organised with specific directories that can be called in a
command line interface (CLI). The structure of the directories is described
in the [Structure](#structure) section below.

The entry point is in `{{cookiecutter.__project_slug}}\src\__main__.py`.
For help with the commands the usual `--help` option is available.

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src --help
```

## How to use the workflow {#work}

**Important**: This section assumes that the default setup is in place as
described in the [Structure](#structure) section below. It can be modified as
described in the [Directories' Specifications](#dir-specs) below but you should
start with the default.

To run the modules in a given directory, for example the *s2_transf* directory,
wou must be in the project directory and use this command

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transf
```

This will run all the files in the *s2_transf* directory in alphabetical order.

To run a specific module in a directory, for example the *transf99a_todo.py* in
the *s2_transf* directory, you can use a regex pattern as follows:

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transf --pat todo
```

We could have used any word that starts with ***tr*** and the `workflow` would
understand it to be for the *s2_transf*. See the [Directories Identifications](#dir-id)
for a table of the directory identifications.

## How to use the workflow for a pipeline {#work-pipe}

Very often, you will probably want to use several directories as in a pipeline.
For example to run the *extract*, *transform* and *load* directories you will
do

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transf,extr,load
```

See the [Directories Identifications](#dir-id) for a table of the directory
identifications that can be used.

**The order is unimportant** because the `workflow` will always run the directories
in the order of their given priorities as set in the ***workflow.json*** file.
See the [Directories Specifications](*dir-specs) section below.

**Only the first two characters of the directory id matter**. For example the
following command would work like the one just mentioned previously.

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transform,ex,LOAD
```

### How to use the pattern

As mentioned in [Workflow](#work) section you can use a regex pattern to run a
specific file. For example

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transf --pat todo
```

would run any file starting with the prefix *transf* and containing *todo*
in its name.

If you use `--pat todo` with several directories in a pipeline, the pattern
will be applied to all directories in the pipeline.


### Directories Identifications {#dir-id}

The task id are 2-letter words used to identify a task.  If a longer word is
used, only the first 2 letters will be used. The **table of task id** is

|name|Priority|Command|Description
|:-----|:-----:|:-----|:-----
|***ex***|1|`extr`|Extract
|***tr***|2|`transf`|Transform
|***lo***|3|`load`|Load
|***ra***|4|`raw`|Raw data
|***pp***|5|`pproc`|Pre-processing
|***ed***|6|`eda`|E.D.A.
|***fi***|7|`final`|Finalize

### Sructure {#structure}

Thie is the default structure of the project. It can be modified in which case
the ***workflow.json*** file must be changed. See the [json](#dir-specs)

```text
{{cookiecutter.__project_slug}}
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
│   ├── d0_temp               <- Temporary folder. These files can be deleted.
│   ├── d1_raw                <- Original, immutable data.
|   ├── d2_transf             <- Data being transformed.
|   ├── d3_ready              <- Transformed data ready to use.
│   ├── d4_preproc            <- Preprocessed data to used for EDA.
│   ├── d5_eda                <- Data used for exploratory data analysis.
│   ├── d6_final              <- Final data sets used for reports.
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
│   ├── workflow.py           <- CLI used by __main__.py to run the modules.
│   ├── workflow.json         <- Directory specifications. Used by workflow.py
│   ├── s0_helpers            <- Utilities and helper codes.
│   │   ├── __init__.py
|   |   └── ...
|   ├── s1_extr               <- Code to extract the raw data.
│   │   ├── __init__.py
|   |   └── ...
|   ├── s2_transf             <- Code to transform the raw data.
│   │   ├── __init__.py
|   |   └── ...
|   ├── s3_load               <- Code to load the raw data, usually in a database.
│   │   ├── __init__.py
|   |   └── ...
|   ├── s4_preproc            <- Code to preprocess the data for EDA.
│   │   ├── __init__.py
|   |   └── ...
|   ├── s5_eda                <- Code for exploratory data analysis.
│   │   ├── __init__.py
|   |   └── ...
|   ├── s6_final              <- Code for final data usually used in reporting.
│   │   ├── __init__.py
|   |   └── ...
|   └── ...
└── tests                     <- All test and fixtures files used in testing.
    ├── __init__.py
    ├── fixtures              <- Where to put example inputs and outputs.
    │   ├── input.json        <- Test input data.
    │   └── output.json       <- Test output data.
    ├── test_extract_acc.py   <- Test example for etl..
    ├── test_samples.py       <- Test example to verify `pytest`.
    └── ...
```

### Directories Specifications {#dir-specs}

The directories' attributes are described in the ***workflow.json*** where every
directory has the following attributes:

priority
: The Integer defining the priority of this directory.

name
: 2-letter word used to define the directory in the command line interface.

label
: A label used when printing information.

prefix
: Prefix used to identify the the modules that will be run in the directories.

dir
: The name of the directory containing the modules to be run.

emo
: Emoji name used to identify the directory.

song:
: Letter to identify sounds associated with the running of the directory.
