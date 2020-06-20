#!/usr/bin/env bash

exec celery -A api.tasks worker --loglevel=info -Q handicap
