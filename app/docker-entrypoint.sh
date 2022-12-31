#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Load datas to PostgreSQL"
cd sqlite_to_postgres/ && python load_data.py

cd ..

# Start server
echo "Starting server"

chown www-data:www-data /var/log

uwsgi --strict --ini uwsgi.ini