#! /usr/bin/env bash

set -e pipefail

SEARCH_ENGINE_URI="http://localhost:9200"
PORT=8001
CONTAINER_NAME="search-service-api"
IMAGE_NAME="search-service-api:latest"

main() {
  docker container run --env "SEARCH_ENGINE_URI=${SEARCH_ENGINE_URI}" -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}
}

main