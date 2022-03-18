#!/bin/bash

docker run --rm -it -v "$(pwd)/:/source" python:3 bash -c "\
    apt-get update; \
    pip install poetry; \
    cd /source; \
    poetry update"
