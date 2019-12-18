#!/usr/bin/env bash
export PYTHONPATH=${PYTHONPATH}:/Users/SilverNarcissus/mindRecipe/worker

python3 worker/manage.py runserver $1
