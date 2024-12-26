#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

DOCKER_IMAGE="python:3.13.1-slim@sha256:1127090f9fff0b8e7c3a1367855ef8a3299472d2c9ed122948a576c39addeaf1"

docker run --rm \
  --pull always \
  -it \
  -v "$(pwd)/:/source" \
  -v "/source/.venv" \
  $DOCKER_IMAGE bash -c "\
    pip install poetry; \
    cd /source; \
    poetry self add poetry-plugin-export; \
    poetry update; \
    poetry lock; \
    poetry export --format requirements.txt --without dev --output /source/requirements.txt; \
    poetry export --format requirements.txt --with dev --output /source/requirements-dev.txt;"
