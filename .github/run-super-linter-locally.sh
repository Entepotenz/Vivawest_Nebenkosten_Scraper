#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

FOLDER_PATH_TO_ANALYZE="$SCRIPT_DIR/../"
FOLDER_PATH_TO_ANALYZE=$(readlink -f "$FOLDER_PATH_TO_ANALYZE")

docker run --rm \
    -e RUN_LOCAL=true \
    --env-file "$SCRIPT_DIR/super-linter-locally.env" \
    -v "$FOLDER_PATH_TO_ANALYZE":/tmp/lint github/super-linter:slim-latest
