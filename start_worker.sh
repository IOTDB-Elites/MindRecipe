#!/usr/bin/env bash
export PYTHONPATH=./worker:${PYTHONPATH}

python3 worker/manage.py runserver $1
