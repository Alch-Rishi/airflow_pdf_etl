#!/bin/bash
export TIKA_SERVER_ADDR=tikaserver
export TIKA_SERVER_PORT=9998
export ELASTIC_SERVER_ADDR=elasticsearch
export ELASTIC_SERVER_PORT=9200


airflow initdb
airflow webserver &

if test -z "${TIKA_SERVER_ADDR}" -o -z "${TIKA_SERVER_PORT}"; then
    echo "You must link this container with TIKA first"
    exit 1
fi

if test -z "${ELASTIC_SERVER_ADDR}" -o -z "${ELASTIC_SERVER_PORT}"; then
    echo "You must link this container with Elastic search first"
    exit 1
fi

export TESTING_TIKA_URL="tcp://${TIKA_SERVER_ADDR}:${TIKA_SERVER_PORT}"
export TESTING_ELASTIC_URL="tcp://${ELASTIC_SERVER_ADDR}:${ELASTIC_SERVER_PORT}"

# See http://tldp.org/LDP/abs/html/devref1.html for description of this syntax.
# while ! exec 6<>/dev/tcp/${TIKA_SERVER_ADDR}/${TIKA_SERVER_PORT}; do
#     echo "$(date) - still trying to connect to TIKA at ${TESTING_TIKA_URL}"
#     sleep 5
# done

# exec 6>&-
# exec 6<&-

# while ! exec 6<>/dev/tcp/${ELASTIC_SERVER_ADDR}/${ELASTIC_SERVER_PORT}; do
#     echo "$(date) - still trying to connect to Elastic search at ${TESTING_ELASTIC_URL}"
#     sleep 10
# done

# exec 6>&-
# exec 6<&-


airflow schedular
#/usr/local/bin/python /usr/local/airflow/dags/test.py 

sleep 300

