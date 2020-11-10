#! /usr/bin/env bash

# should be run from top-level directory in repo
main() {
  test_directory=$(pwd)/lambdas/handicap-service
  PYTHONPATH="${test_directory}/src" python -m pytest -m "not integration" "${test_directory}"
}

main
