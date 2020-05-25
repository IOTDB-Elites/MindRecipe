#!/usr/bin/env bash
export PYTHONPATH=./worker:${PYTHONPATH}

python3.6 worker/manage.py runserver $1 $2
