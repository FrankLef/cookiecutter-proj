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

## Concept and Usage

The project is organized around the concept that

* The work is done is 7 steps group in 2 stages
  * Extract, transfer and load data (EDA) then
  * Do an exploratory data analysis (EDA).
* Every step is associated with
  * a dedicated module and a
  * dedicated data set

The command, source code location and data location associated with evert step
is summarized in the following table.

|Command|Source Code|Data Set|Description
|:-----|:-----|:-----|:-----|
|extr|s1_extr|d1_extr|Extract data from an external source|
|transf|s2_transf|d2_transf|Tranform the extracted data to a table format|
|load|s3_load|d3_load|Upload to an external database|
|raw|s4_raw|d4_raw|Get raw data for EDA|
|pproc|s5_pproc|d5_pproc|Preprocess data for EDA|
|eda|s6_eda|d6_eda|Exploratory Data Analysis|
|final|s7_final|d7_final|Finalize EDA|

To run a given *ETL* step, for example the *extract* you would do

```console
cd ..\{{cookiecutter.__project_slug}}
poetry run python -m src etl extr <subprocess>
```

where *subprocess* is a string identiying a subprocess.

To run a given *EDA* step, for example the *raw* you would do

```console
cd ..\{{cookiecutter.__project_slug}}
poetry run python -m src eda raw <subprocess>
```

where *subprocess* is a string identiying a subprocess.
