#!/bin/bash

set -x
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "${SCRIPT_DIR}/pass.sh"

docker run --rm -it -v "${SCRIPT_DIR}:/app" -p 127.0.0.1:80:8080 python:3 bash -c "\
    apt-get update \
        && apt-get -y install gcc make chromium chromium-driver \
        && rm -rf /var/lib/apt/lists/*s; \
    pip install --no-cache-dir --upgrade pip; \
    pip install poetry; \
    cd /app; \
    poetry install; \
    cd /app/source; \
    USERNAME=\"${USERNAME}\" PASSWORD=\"${PASSWORD}\" poetry run gunicorn --bind 0.0.0.0:8080 --timeout 90 --reload app:app"