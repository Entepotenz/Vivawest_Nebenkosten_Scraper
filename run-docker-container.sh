#!/bin/bash

set -x
set -e

readonly SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
readonly DOCKER_IMAGE_NAME="vivawest_scraper"
readonly PATH_TO_DOCKERFILE="${SCRIPT_DIR}/Dockerfile"

touch "${SCRIPT_DIR}/pass.sh"
chmod u=rw,g=,o= "${SCRIPT_DIR}/pass.sh"

if [ "$#" -eq 1 ]; then
    if [[ -n "$1" ]]; then
        if [ "$1" = "rebuild" ]; then
            docker image rm $(docker images | tr -s ' ' : | grep ${DOCKER_IMAGE_NAME} | cut -f3 -d:)
            docker build -t "${DOCKER_IMAGE_NAME}" --file "${PATH_TO_DOCKERFILE}" .
        else
            echo "\"$1\" -> unsupported argument"
        fi
    fi
fi

if [[ "$(docker images -q "${DOCKER_IMAGE_NAME}" 2> /dev/null)" == "" ]]; then
  docker build -t "${DOCKER_IMAGE_NAME}" --file "${PATH_TO_DOCKERFILE}" .
fi

docker run --rm "${DOCKER_IMAGE_NAME}"