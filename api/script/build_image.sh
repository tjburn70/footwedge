#! /usr/bin/env bash

set -e pipefail

DOCKER_REPO="tjburn70/footwedge"
TAG="api-latest"
IMAGE_NAME="${DOCKER_REPO}:${TAG}"

main() {
  echo "building ${IMAGE_NAME} docker image"
  docker build --file ./Dockerfile --tag ${IMAGE_NAME} .
}

main