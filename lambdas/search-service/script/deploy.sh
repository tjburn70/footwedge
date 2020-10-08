#! /usr/bin/env bash

STAGE=$1
AWS_REGION=$2

if [[ -z "${STAGE}" ]]; then
  echo "Please specify a stage/environment you want to deploy to"
  exit 1
fi

if [[ -z "${AWS_REGION}" ]]; then
  echo "Please specify an AWS region you want to deploy to"
  exit 1
fi

main() {
  serverless deploy --stage "${STAGE}" --region "${AWS_REGION}"
}

main
