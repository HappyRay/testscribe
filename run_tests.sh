#!/bin/env bash

# turn on echo
set -x

# The working directory is assumed to be the project root
export PYTHONPATH="$PYTHONPATH:src:tests"

if [ "$1" == "-c" ]; then
  # -c option to turn on code coverage
  # generate the output to a directory outside the source and test directories
  COVERAGE_ARG="--cov-report html:tmp/test-coverage --cov-report xml:tmp/cov.xml --cov=src/testscribe --cov-config=.coveragerc"
  shift
else
  COVERAGE_ARG=""
fi

if [ "$1" != "" ]; then
    TARGET=$1
else
    TARGET="tests"
fi
#pytest -vv test_end_to_end.py

poetry run pytest $COVERAGE_ARG -vv $TARGET