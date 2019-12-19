#!/usr/bin/env bash
export PYTHONPATH=./master:${PYTHONPATH}

python3 master/manage.py runserver $1
