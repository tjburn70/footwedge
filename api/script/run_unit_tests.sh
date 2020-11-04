#! /usr/bin/env bash

# should be run from top-level directory in repo
main() {
  test_directory=$(pwd)/api
  PYTHONPATH="${test_directory}" python -m pytest "${test_directory}"
}

main