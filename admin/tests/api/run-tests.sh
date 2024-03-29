#!/usr/bin/env bash

set -e

WAIT_UNTIL=$(expr $(date +%s) + 600)

echo "Waiting for Redis to be initialized"
while [[ $(docker exec -i redis redis-cli -p 7000 ping) != "PONG" ]]
do
    CURRENT_TIME=$(date +%s)
    if [ $CURRENT_TIME \> $WAIT_UNTIL ]; then
        echo "Timeout reached while waiting for Redis to initialize. Exiting with failure..."
        exit 1
    fi

    echo "Still waiting for Redis to be initialized"
    sleep 5
done

echo "Waiting for MySQL to be initialized"
while [[ $(docker exec -i mysql mysqladmin -h 127.0.0.1 -uroot -ptest ping) != "mysqld is alive" ]]
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

PYTHONPATH=./admin MYSQL_ECHO=0 python -m pytest --disable-warnings --cov=./app --cov-fail-under=80 --no-cov-on-fail ./tests/api

# Reset DBs
docker exec -i mysql bash /docker-entrypoint-initdb.d/init.sh
docker exec -i redis redis-cli --cluster call 127.0.0.1:7000 FLUSHALL
