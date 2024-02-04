#!/usr/bin/env bash

WAIT_UNTIL=$(expr $(date +%s) + 600)

echo "Waiting for Redis to be initialized"
while [[ $(redis-cli -p 7000 ping) != "PONG" ]]
do
    CURRENT_TIME=$(date +%s)
    if [ $CURRENT_TIME \> $WAIT_UNTIL ]; then
        echo "Timeout reached while waiting for Redis to initialize. Exiting with failure..."
        exit 1
    fi

    echo "Still waiting for Redis to be initialized"
    sleep 5
done

sleep 5

PYTHONPATH=./flags MYSQL_ECHO=0 python -m pytest --disable-warnings --cov=./flags/app --cov-fail-under=80 --no-cov-on-fail ./flags/tests/api

redis-cli --cluster call --cluster-only-masters 127.0.0.1:7000 FLUSHALL
