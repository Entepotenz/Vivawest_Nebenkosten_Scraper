#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

DOCKER_IMAGE="python:3.14.2-slim@sha256:3955a7dd66ccf92b68d0232f7f86d892eaf75255511dc7e98961bdc990dc6c9b"

if ! command -v pylint &>/dev/null; then
  docker run --rm -it -v "$(pwd)/source:/source" \
    $DOCKER_IMAGE bash -c "\
        pip install pylint; \
        pylint /source"
else
  pylint "$SCRIPT_DIR/source"
fi
