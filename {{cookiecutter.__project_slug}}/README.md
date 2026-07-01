# {{cookiecutter.project_name}}

<!-- badges: start -->
[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
<!-- badges: end -->

## Introduction

This is the main *readme* of the {{cookiecutter.project_name}} project.

The sections below cover the `workflow` command to
run the project modules as a pipeline in a very simple and straightforward way.

## Workflow

The project is organised with specific directories that can be called in a
command line interface (CLI). The structure of the directories is described
in the [Directory Structure](#directory-structure) section below.

The entry point is in `{{cookiecutter.__project_slug}}\src\__main__.py`.
For help with the commands the usual `--help` option is available.

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src --help
```

## How to use the workflow

**Important**: This section assumes that the default directories are in place as
described in the [Directory Structure](#directory-structure) section below.
It can be modified as described in the [Configuration](#configuration) below but you should
start with the default.

To run the modules in a given directory, for example the *s2_transf* directory,
wou must be in the project directory and use this command

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transf
```

This will run all the files whose name begins with the prefix **run** in the
*s2_transf* directory in alphabetical order.

To run a specific module in a directory, for example to run *run99a_todo.py* in
the *s2_transf* directory, you can use a regex pattern as follows:

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transf --pat todo
```

We could have used any word that starts with ***tr*** and the `workflow` would
understand it to be for the *s2_transf*. See the [Directories](#directories)
section for a table of the directory identifications.

## How to use the workflow for a pipeline

Very often, you will probably want to use several directories as in a pipeline.
For example to run the *extract*, *transform* and *load* directories you will
do

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transf,extr,load
```

See the [Directories](#directories) section for a table of the directory
identifications that can be used.

**The order is unimportant** because the `workflow` will always run the directories
in the order of their given priorities as set in the **config.json*** file.
See the [Configuration](#configuration) section below for information on the directories.

**Only the first two characters of the directory id matter**. For example the
following command would work like the one just mentioned previously.

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transform,ex,LOAD
```

### How to use the pattern

As mentioned in the above section you can use a regex pattern to run a
specific file. For example

```console
cd ..\{{cookiecutter.__project_slug}}
python -m src pipe transf --pat todo
```

would run any file starting with the prefix *transf* and containing *todo*
in its name.

If you use `--pat todo` with several directories in a pipeline, the pattern
will be applied to all directories in the pipeline.

### Configuration

The few configuration settings are located in the `.\_workflow\config.json`.
This config file has 3 setions only.

#### run_prefix

This section identifies the word used as a prefix in the file names to select the module
that will be run. The default is **run** and it is recommended not to change that
unless there is a pretty good reason to do so.

#### success_wav

This section identifies the name of the sound file used to generate a sound when a run
is successfully completed. The file must be located in the `.\_worklow` directory.

#### dirs

This section identifies the different directories that will be run by the worklow.

Each directory's specifications includes

* **priority**: Detrmine the order in which the directory will be run.
* **name**: The 2-character, and *unique* word used to run the given directory. See [Directories](#directories).
* **emo**: The emoji name used in the CLI.
* **song**: The name of the sound used to identify the directory. To be used (maybe) in the future.

### Directories

The task id are 2-letter words used to identify a task as discussed in the
[dirs](#dirs) section just above.  If a longer word is used, only the first
2 letters will be used. The **table of directories** is

Priority|Name|Dir|Description
:-----|:-----:|:-----|:-----
0|***se***|`s0_setup`|Set up
1|***ex***|`s1_extr`|Extract
2|***tr***|`s2_transf`|Transform
3|***lo***|`s3_load`|Load
4|***ra***|`s4_raw`|Raw data
5|***pp***|`s5_pproc`|Pre-processing
6|***ed***|`s6_eda`|E.D.A.
9|***te***|`s9_teard`|Tear down

### Directory Structure

This is the default structure of the project. It can be modified in which case
the `.\_worklow\config.json` file must be changed.
See the [Configuration](#configuration) section above.

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
│   ├── _workflow             <- CLI used by __main__.py to run the modules.
|   |   ├── config.json       <- Configuration file used by `workflow`.
|   |   └── ...
│   ├── s0_setup              <- Code used for setting up the project.
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
|   ├── s5_eda                <- Code for exploratory data analysis (EDA).
│   │   ├── __init__.py
|   |   └── ...
|   ├── s9_teard              <- Code used to tear down the project.
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
