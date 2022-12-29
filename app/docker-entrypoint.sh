#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"

chown www-data:www-data /var/log

uwsgi --strict --ini uwsgi.ini