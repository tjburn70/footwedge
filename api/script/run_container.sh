#! /usr/bin/env bash

set -e pipefail

AWS_REGION="us-east-2"
PORT=8000
CONTAINER_NAME="footwedge-api"
IMAGE_NAME="footwedge-api:latest"

main() {
  docker container run --env "AWS_DEFAULT_REGION=${AWS_REGION}" -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}
}

main