#!/bin/bash
app_concurrent_workers=8
web_server_port=8000

echo "start make migrations"
python manage.py migrate
echo "finish migrations"

echo "start collect static files"
python manage.py collectstatic --noinput
echo "finish collect static files"

echo "Run server"
gunicorn --bind 0.0.0.0:"$web_server_port" ecommerce.wsgi -w "$app_concurrent_workers" --access-logfile '-' &

wait