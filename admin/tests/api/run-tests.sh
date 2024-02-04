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

PYTHONPATH=./admin MYSQL_ECHO=0 python -m pytest --disable-warnings --cov=./admin/app --cov-fail-under=80 --no-cov-on-fail ./admin/tests/api

# Reset DBs
docker exec -i mysql bash /docker-entrypoint-initdb.d/init.sh
redis-cli --cluster call --cluster-only-masters 127.0.0.1:7000 FLUSHALL
