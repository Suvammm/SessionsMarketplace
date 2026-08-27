#!/bin/sh
set -e
until python manage.py migrate --noinput; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done
python manage.py collectstatic --noinput
exec "$@"
