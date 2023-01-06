#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

readonly SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if ! command -v pylint &> /dev/null; then
    docker run --rm -it -v "$(pwd)/source:/source" python:3-slim bash -c "\
        pip install --upgrade pip; \
        pip install pylint; \
        pylint /source"
else
    pylint "${SCRIPT_DIR}/source"
fi
