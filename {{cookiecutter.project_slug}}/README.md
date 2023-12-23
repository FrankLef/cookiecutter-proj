# {{ cookiecutter.project_name }}

<!-- badges: start -->
[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
<!-- badges: end -->

## Introduction

{{ cookiecutter.description }}

## Pipeline

The pipeline can be run by changing to the src

    cd src

and usin the command

    python cli.py <start>

where `start` is where the pipeline starts. It must one of
`("etl", "preproc", "feat", "model", "windup")`. See help for more details.

    pythin cli.py -h
