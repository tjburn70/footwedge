#! /usr/bin/env bash

# should be run from top-level directory in repo
main() {
  echo $(pwd)
  test_directory=$(pwd)/lambdas/search-service
  PYTHONPATH="${test_directory}/src" python -m pytest "${test_directory}"
}

main
