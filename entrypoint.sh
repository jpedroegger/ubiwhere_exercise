#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."

until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - applying migrations..."
python manage.py migrate

echo "Starting Django server..."
exec "$@"
