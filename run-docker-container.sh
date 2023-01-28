#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
readonly DOCKER_IMAGE_NAME="vivawest_scraper"
readonly PATH_TO_DOCKERFILE="$SCRIPT_DIR/Dockerfile"
readonly PATH_TO_PASS_SH="$SCRIPT_DIR/pass.sh"
readonly PATH_TO_SOURCE_FOLDER="$SCRIPT_DIR/source/"

touch "$PATH_TO_PASS_SH"
chmod u=rw,g=,o= "$PATH_TO_PASS_SH"

if [ "$#" -eq 1 ]; then
    if [[ -n "$1" ]]; then
        if [ "$1" = "rebuild" ]; then
          if docker images | tr -s ' ' : | grep -q "$DOCKER_IMAGE_NAME"; then
            images_to_delete=$(docker images | tr -s ' ' : | grep $DOCKER_IMAGE_NAME | cut -f3 -d:)
            for image_id in $images_to_delete; do
              docker image rm "$image_id"
            done
          fi
          docker build -t "$DOCKER_IMAGE_NAME" --file "$PATH_TO_DOCKERFILE" .
        else
            echo "\"$1\" -> unsupported argument"
        fi
    fi
fi

if [[ "$(docker images -q "$DOCKER_IMAGE_NAME" 2> /dev/null)" == "" ]]; then
  docker build -t "$DOCKER_IMAGE_NAME" --file "$PATH_TO_DOCKERFILE" .
fi

docker run --rm -v "$PATH_TO_PASS_SH:/app/pass.sh:ro" -v "$PATH_TO_SOURCE_FOLDER:/app/source/" "$DOCKER_IMAGE_NAME"