#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

DOCKER_IMAGE="python:3.14.2-slim@sha256:2751cbe93751f0147bc1584be957c6dd4c5f977c3d4e0396b56456a9fd4ed137"

if ! command -v pylint &>/dev/null; then
  docker run --rm -it -v "$(pwd)/source:/source" \
    $DOCKER_IMAGE bash -c "\
        pip install pylint; \
        pylint /source"
else
  pylint "$SCRIPT_DIR/source"
fi
