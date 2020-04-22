#!/usr/bin/env bash

export PORT=8000
exec gunicorn api.index:app --name all-square-api -b 127.0.0.1:$PORT -w 1 --threads 2 -t 60
