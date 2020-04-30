#!/usr/bin/env bash

cd "$(dirname "$0")"
cd ..

echo "Building api image..."
exec docker build --file ./Dockerfile-api --tag footwedge-api:latest .
