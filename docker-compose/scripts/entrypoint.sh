#!/bin/bash

# make migration
#!/bin/bash

# Si le conteneur est "web1", il fait les migrations
if [ "$SERVER_NAME" = "web1" ]; then
    echo "Running migrations from web1..."
    python manage.py migrate --noinput
fi

echo "Starting server on 0.0.0.0:8000..."

exec gunicorn application_web.wsgi:application --bind 0.0.0.0:8000
