#!/bin/sh

if [ "$DJANGOCONSULTATIONS_DB_ENGINE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DJANGOCONSULTATIONS_DB_HOST $DJANGOCONSULTATIONS_DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"