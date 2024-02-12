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

# Add up some redis data
redis-cli -c --cluster call --cluster-only-masters 127.0.0.1:7000 FLUSHALL
redis-cli -c --cluster call --cluster-only-masters 127.0.0.1:7000 HSET "context-fields:{1}" "str" "1"
redis-cli -c --cluster call --cluster-only-masters 127.0.0.1:7000 HSET "feature-flags:{1}" "FLAG_1" '[[{"context_key": "str", "operator": 1, "value": "abc"}]]'
redis-cli -c --cluster call --cluster-only-masters 127.0.0.1:7000 SADD "private-keys:{1}" "gAAAAABlyKFJOkSChKo00njI-gPRHdR96V0xcykwHeim2qTJ_IYaQ00kyaDRIXv6r-Rzg2Yi1eXI5ZeCskrcq1WGow51djuyCEhEfcWLaD8amAtIW5EKTxj88Aa5f2yqlUlYryiM3lTJ-5qipYOM-6aWrzp9bC3iLFJ7svGpifl6AtpwnYZuod0="

PYTHONPATH=./flags MYSQL_ECHO=0 python -m pytest --disable-warnings --cov=./flags/app --cov-fail-under=50 --no-cov-on-fail ./flags/tests/api

redis-cli -c --cluster call --cluster-only-masters 127.0.0.1:7000 FLUSHALL
