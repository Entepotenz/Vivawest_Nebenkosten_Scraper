#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

DOCKER_IMAGE="python:3.12.4-slim@sha256:f11725aba18c19664a408902103365eaf8013823ffc56270f921d1dc78a198cb"

if ! command -v yapf &>/dev/null; then
  docker run --rm -it -v "$(pwd)/source:/source" $DOCKER_IMAGE bash -c "\
        pip install yapf; \
        yapf --style google -ir /source"
else
  yapf --style google -ir "$SCRIPT_DIR/source"
fi

if ! command -v black &>/dev/null; then
  docker run --rm -it -v "$(pwd)/source:/source" $DOCKER_IMAGE bash -c "\
        apt-get update && apt-get install -y --no-install-recommends build-essential; \
        pip install black; \
        black /source"
else
  black "$SCRIPT_DIR/"
fi
