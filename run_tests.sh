#!/bin/env bash

# turn on echo
set -x

# python tests expect the working directory to be tests
cd tests
export PYTHONPATH="$PYTHONPATH:src"

if [ "$1" == "-c" ]; then
  # -c option to turn on code coverage
  # generate the output to a directory outside the source and test directories
  COVERAGE_ARG="--cov-report html:../tmp/test-coverage --cov=../src/test_scribe"
  shift
else
  COVERAGE_ARG=""
fi

if [ "$1" != "" ]; then
    TARGET=$1
else
    TARGET="."
fi
#pytest -vv test_end_to_end.py

poetry run pytest $COVERAGE_ARG -vv $TARGET