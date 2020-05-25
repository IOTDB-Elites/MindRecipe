#!/usr/bin/env bash
export PYTHONPATH=./master:${PYTHONPATH}

python3.6 master/manage.py runserver $1
