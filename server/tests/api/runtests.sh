#!/bin/sh

CONTAINER="mysql"
USERNAME="root"
PASSWORD="mysql1234"
echo "Checking if MySQL is up and running..."
while ! docker exec $CONTAINER mysql -u$USERNAME -p$PASSWORD -e "SELECT 1" >/dev/null 2>&1; do
    sleep 5
    echo "Retrying..."
done

PYTHONPATH=./server python -m pytest -p no:warnings server/tests/api
