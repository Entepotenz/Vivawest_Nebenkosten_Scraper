#!/bin/bash

if ! command -v yapf &> /dev/null; then
    docker run --rm -it -v "$(pwd)/source:/source" python:3 bash -c "\
        apt-get update; \
        pip install yapf; \
        yapf --style google -ir /source"
else
    yapf --style google -ir ./source
fi
