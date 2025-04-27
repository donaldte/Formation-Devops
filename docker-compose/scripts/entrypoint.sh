#!/bin/bash

# make migration
echo "Running migrations..."
python manage.py migrate

echo "Starting server on 0.0.0.0:8000..."

exec gunicorn dapplication_web.wsgi:application --bind 0.0.0.0:8000
