#! /usr/bin/env bash

set -e pipefail

IMAGE_NAME="footwedge:search-service-api-latest"

main() {
  echo "building ${IMAGE_NAME} docker image"
  docker build --file ./Dockerfile --tag ${IMAGE_NAME} .
}

main