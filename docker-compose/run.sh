#!/bin/bash

echo "Starting server on 0.0.0.0:8000..."

exec gunicorn app.wsgi:application --bind 0.0.0.0:8000
