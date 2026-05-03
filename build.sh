#!/bin/bash
# build.sh

echo "Building project..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Applying migrations..."
python manage.py migrate --noinput