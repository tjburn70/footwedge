#!/usr/bin/env bash

STAGE=$1
AWS_REGION=$2

main() {
  cd ./lambdas
  cd ./handicap-service

  echo "Deploying Lambdas..."
  serverless deploy --stage "${STAGE}" --region "${AWS_REGION}"
}

main
