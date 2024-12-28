# {{cookiecutter.__title_name}}

<!-- badges: start -->
[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
<!-- badges: end -->

## Introduction

`{{ cookiecutter.description }}` objectives are to

* extract, transform and load data (ETL)
* do an exploratory data analysis (EDA)

## How to use

The entry point is in `{{cookiecutter.__project_slug}}\src\__main__.py`.
For help with the commands the usual `--help` option is available.

```console
cd ..\{{cookiecutter.__project_slug}}
poetry run python -m src etl --help
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
