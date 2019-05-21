#!/bin/bash -xe

PYTHON_EXECUTABLE=${PYTHON_EXECUTABLE:-"/usr/bin/env python3.6"}

if [ -n "${DB_USER}" -a -n "${DB_PASSWORD}" -a -n "${MSP_DOCKER_IP}" ]; then
    DB_PORT=${DB_PORT:-5432}

    for entry in $(${PYTHON_EXECUTABLE} ../manage.py discover_postgres_service); do
        IFS=":" read -r -a ARRAY <<< "${entry}"
        ./liquibase --url=jdbc:postgresql://${ARRAY[0]}:${DB_PORT}/${ARRAY[1]} \
                    --classpath=jdbcdrivers/postgresql-42.2.5.jar \
                    --username="${DB_USER}" \
                    --password="${DB_PASSWORD}" \
                    --changeLogFile=changelog.xml \
                    --logLevel=warning \
                    "${@}"
    done
else
	echo "You should specify all variables: DB_USER, DB_PASSWORD, MSP_DOCKER_IP"
	exit 1
fi
