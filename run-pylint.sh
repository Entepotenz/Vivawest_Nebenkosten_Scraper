#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if ! command -v pylint &> /dev/null; then
    docker run --rm -it -v "$(pwd)/source:/source" python:3 bash -c "\
        apt-get update; \
        pip install pylint; \
        pylint /source"
else
    pylint "${SCRIPT_DIR}/source"
fi
