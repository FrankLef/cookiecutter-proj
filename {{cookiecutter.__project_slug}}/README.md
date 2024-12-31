# Pjrl

<!-- badges: start -->
[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
<!-- badges: end -->

## Introduction

`{{cookiecutter.__project_slug}}` objectives are to

* extract, transform and load data (ETL)
* do an exploratory data analysis (EDA)

## How to use

The entry point is in `{{cookiecutter.__project_slug}}\src\__main__.py`.
For help with the commands the usual `--help` option is available.

```console
cd ..\{{cookiecutter.__project_slug}}
poetry run python -m src --help
```

## Concept

The project is organized around the concept that

* The work is done is 7 steps group in 2 stages
  * ETL: Extract, transfer and load data
  * EDA: Exploratory data analysis
* Every step is associated with
  * a dedicated module and a
  * dedicated data set

## Usage

**Important**: This section describes the command to use on their own. Am easier
way which allows to run these commands in a pipe can be found at [pipe](#Pipe)
below.

The command, source code location and data location associated with every step
is summarized in the following table.

|Stage|Label|Command|Source Code|Data Set|Description
|:-----|:-----|:-----|:-----|:-----|:-----
|ETL|Extract|`extr`|..\s1_extr|..\d1_extr|Extract data from an external source
|ETL|Transform|`transf`|..\s2_transf|..\d2_transf|Tranform the extracted data to a table format
|ETL|Load|`load`|..\s3_load|..\d3_load|Upload to an external database
|EDA|Raw|`raw`|..\s4_raw|..\d4_raw|Get raw data for EDA
|EDA|Preprocessing|`pproc`|..\s5_pproc|..\d5_pproc|Preprocess data for EDA
|EDA|E.D.A.|`eda`|..\s6_eda|..\d6_eda|Exploratory Data Analysis
|EDA|Final|`final`|..\s7_final|..\d7_final|Finalize EDA

To run a given command, you do

```console
cd ..\{{cookiecutter.__project_slug}}
poetry run python -m src <command> --subproc <subprocess>
```

* `poetry run` is required when you have a package, for example an ***editable
package*** installed in the virtual environment,
* `subproc` is an optional string identifying a subprocess to be used by
the command.

for example the *extract* command `extr` with the subprocess *test* would be

```console
cd ..\{{cookiecutter.__project_slug}}
poetry run python -m src extr --subproc test
```

## Pipe

The `pipe` command allows to process commands, called *tasks* in this context,
in a chain using a comma-delimited string with an id for each task. The `pipe` 
command syntax is

```console
poetry run python -m src pipe <tasks> --subproc <subproc>
```

For example to `extract` then `transform` a subprocess called `test` we would
use

```console
poetry run python -m src pipe extract,transform --subproc test
```

To get help you can use

```console
poetry run python -m src pipe --help
```

### Task id

The task id are 2-letter words used to identify a task.  If a longer word is
used, only the first 2 letters will be used. The **table of task id** is

|id|Sequence|Command|Description
|:-----|:-----:|:-----|:-----
|***ex***|1|`extr`|Extract
|***tr***|2|`transf`|Transform
|***lo***|3|`load`|Load
|***ra***|4|`raw`|Raw data
|***pp***|5|`pproc`|Pre-processing
|***ed***|6|`eda`|E.D.A.
|***fi***|7|`final`|Finalize

The commands are the same as found in [usage](#Usage) above.

For example the command

```console
poetry run python -m src pipe extract,transform --subproc test
```

is the same as

```console
poetry run python -m src pipe ex,tr --subproc test
```

The task ids are arranged in a comma-separated string with the following rules:

* The first 2 letters of task id must be an allowed id, see the table of task
id above for the allowed id.
* The tasks can be in any order. Internally they are run in the sequence shown
in the table of task id above.
* All spaces will be removed.
* The tasks string is case-insensitive.

For example the command

```console
poetry run python -m src pipe TRANSForm,loDAing,extract --subproc test
```

is processed internally as

```console
poetry run python -m src pipe ex,tr,lo --subproc test
```
