#!/bin/bash

if ! command -v pylint &> /dev/null; then
    docker run --rm -it -v "$(pwd)/source:/source" python:3 bash -c "\
        apt-get update; \
        pip install pylint; \
        pylint /source"
else
    pylint ./source
fi
