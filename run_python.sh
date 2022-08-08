#!/bin/env bash

cd python/tests
export PYTHONPATH="$PYTHONPATH:../src"

# not sure why using poetry run will result in a permission error.
#poetry run $@
python $@