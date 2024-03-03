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

sleep 5

# Add up some redis data
docker exec -i redis redis-cli -c --cluster call 127.0.0.1:7000 FLUSHALL
docker exec -i redis redis-cli -c --cluster call 127.0.0.1:7000 HSET "context-fields:{1}" "str" "1"
docker exec -i redis redis-cli -c --cluster call 127.0.0.1:7000 HSET "feature-flags:{1}" "FLAG_1" '[[{"context_key": "str", "operator": 1, "value": "abc"}]]'
docker exec -i redis redis-cli -c --cluster call 127.0.0.1:7000 SADD "private-keys:{1}" "gAAAAABlyKFJOkSChKo00njI-gPRHdR96V0xcykwHeim2qTJ_IYaQ00kyaDRIXv6r-Rzg2Yi1eXI5ZeCskrcq1WGow51djuyCEhEfcWLaD8amAtIW5EKTxj88Aa5f2yqlUlYryiM3lTJ-5qipYOM-6aWrzp9bC3iLFJ7svGpifl6AtpwnYZuod0="

PYTHONPATH=./flags MYSQL_ECHO=0 python -m pytest --disable-warnings --cov=./app --cov-fail-under=50 --no-cov-on-fail ./tests/api

docker exec -i redis redis-cli -c --cluster call 127.0.0.1:7000 FLUSHALL
