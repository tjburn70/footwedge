#! /usr/bin/env bash

set -e pipefail

IMAGE_NAME="footwedge:web-client-latest"

main() {
  echo "building ${IMAGE_NAME} docker image"
  docker build --file ./Dockerfile --tag ${IMAGE_NAME} .
}

main