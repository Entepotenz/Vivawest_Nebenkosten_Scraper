#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

DOCKER_IMAGE="python:3.12.3-slim@sha256:afc139a0a640942491ec481ad8dda10f2c5b753f5c969393b12480155fe15a63"

# shellcheck disable=SC1091
source "$SCRIPT_DIR/pass.sh"

docker run --rm -it -v "$SCRIPT_DIR:/app" -v "/app/.venv" -p 127.0.0.1:80:8080 \
  $DOCKER_IMAGE bash -c "\
    apt-get update \
        && apt-get -y install locales gcc make chromium chromium-driver --no-install-recommends \
        && sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen \
        && dpkg-reconfigure --frontend=noninteractive locales \
        && rm -rf /var/lib/apt/lists/*s; \
    export LANG=\"de_DE.UTF-8\"; \
    export LC_ALL=\"de_DE.UTF-8\"; \
    pip install poetry; \
    cd /app; \
    poetry install; \
    cd /app/source; \
    USERNAME=\"${USERNAME}\" PASSWORD=\"${PASSWORD}\" poetry run gunicorn --bind 0.0.0.0:8080 --timeout 90 --reload app:app"
