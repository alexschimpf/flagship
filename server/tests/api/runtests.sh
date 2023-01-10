#!/bin/sh

# TODO: Check if MongoDB container is up and running

PYTHONPATH=./server python -m pytest -p no:warnings server/tests/api
