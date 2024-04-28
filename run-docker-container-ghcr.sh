#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
readonly DOCKER_IMAGE_NAME="ghcr.io/entepotenz/vivawest_nebenkosten_scraper:latest"
readonly PATH_TO_PASS_SH="$SCRIPT_DIR/pass.sh"

docker run --rm --pull always -v "$PATH_TO_PASS_SH:/app/pass.sh:ro" "$DOCKER_IMAGE_NAME"
