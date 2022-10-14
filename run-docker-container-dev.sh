#!/bin/bash

set -x
set -e

readonly SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "${SCRIPT_DIR}/pass.sh"

docker run --rm -it -v "${SCRIPT_DIR}:/app" -p 127.0.0.1:80:8080 python:3-slim bash -c "\
    apt-get update \
        && apt-get -y install locales gcc make chromium chromium-driver --no-install-recommends \
        && sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen \
        && dpkg-reconfigure --frontend=noninteractive locales \
        && rm -rf /var/lib/apt/lists/*s; \
    export LANG=\"de_DE.UTF-8\"; \
    export LC_ALL=\"de_DE.UTF-8\"; \
    pip install --no-cache-dir --upgrade pip; \
    pip install poetry; \
    cd /app; \
    poetry install; \
    cd /app/source; \
    USERNAME=\"${USERNAME}\" PASSWORD=\"${PASSWORD}\" poetry run gunicorn --bind 0.0.0.0:8080 --timeout 90 --reload app:app"
