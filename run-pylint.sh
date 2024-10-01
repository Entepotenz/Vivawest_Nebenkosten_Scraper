#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

DOCKER_IMAGE="python:3.12.6-slim@sha256:ad48727987b259854d52241fac3bc633574364867b8e20aec305e6e7f4028b26"

if ! command -v pylint &>/dev/null; then
  docker run --rm -it -v "$(pwd)/source:/source" \
    $DOCKER_IMAGE bash -c "\
        pip install pylint; \
        pylint /source"
else
  pylint "$SCRIPT_DIR/source"
fi
