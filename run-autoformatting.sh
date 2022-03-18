#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if ! command -v yapf &> /dev/null; then
    docker run --rm -it -v "$(pwd)/source:/source" python:3 bash -c "\
        apt-get update; \
        pip install yapf; \
        yapf --style google -ir /source"
else
    yapf --style google -ir "${SCRIPT_DIR}/source"
fi

if ! command -v black &> /dev/null; then
    docker run --rm -it -v "$(pwd)/source:/source" python:3 bash -c "\
        apt-get update; \
        pip install black; \
        black /source"
else
    black "${SCRIPT_DIR}/source"
fi
