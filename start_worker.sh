#!/usr/bin/env bash
export PYTHONPATH=${PYTHONPATH}:./worker

python3 worker/manage.py runserver $1
