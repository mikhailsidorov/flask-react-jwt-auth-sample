#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD="$DB_ROOT_PASS" psql -h "$DB_HOST" -U "$DB_ROOT" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
