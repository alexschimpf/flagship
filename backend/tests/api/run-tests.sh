#!/usr/bin/env bash

WAIT_UNTIL=$(expr $(date +%s) + 600)

echo "Waiting for MySQL to be initialized"
while [[ $(mysqladmin -h 127.0.0.1 -uroot -ptest ping) != "mysqld is alive" ]]
do
    CURRENT_TIME=$(date +%s)
    if [ $CURRENT_TIME \> $WAIT_UNTIL ]; then
        echo "Timeout reached while waiting for MySQL to initialize. Exiting with failure..."
        exit 1
    fi

    echo "Still waiting for MySQL to be initialized"
    sleep 5
done

sleep 5

PYTHONPATH=./backend MYSQL_ECHO=0 python -m pytest --disable-warnings --cov=./backend/app --cov-fail-under=80 --no-cov-on-fail ./backend/tests/api