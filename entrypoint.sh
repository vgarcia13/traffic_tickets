#!/bin/bash

# make database migrations
echo "Make database migrations"
python manage.py makemigrations --merge

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000