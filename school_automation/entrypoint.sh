#!/bin/sh

# while ! mysqladmin ping -h"mysql" --silent; do
#     echo "Waiting for MySQL..."
#     sleep 2
# done
echo "Apply database migrations"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Creating superuser"
python3 manage.py createsuperuser --noinput --phone_number "$DJANGO_SUPERUSER_PHONE_NUMBER"

exec "$@"