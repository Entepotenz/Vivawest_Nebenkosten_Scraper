#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

DOCKER_IMAGE="python:3.13.1-slim@sha256:f41a75c9cee9391c09e0139f7b49d4b1fbb119944ec740ecce4040626dc07bed"

if ! command -v pylint &>/dev/null; then
  docker run --rm -it -v "$(pwd)/source:/source" \
    $DOCKER_IMAGE bash -c "\
        pip install pylint; \
        pylint /source"
else
  pylint "$SCRIPT_DIR/source"
fi
