#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

DOCKER_IMAGE="python:3.14.3-slim@sha256:5e59aae31ff0e87511226be8e2b94d78c58f05216efda3b07dbbed938ec8583b"

if ! command -v pylint &>/dev/null; then
  docker run --rm -it -v "$(pwd)/source:/source" \
    $DOCKER_IMAGE bash -c "\
        pip install pylint; \
        pylint /source"
else
  pylint "$SCRIPT_DIR/source"
fi
