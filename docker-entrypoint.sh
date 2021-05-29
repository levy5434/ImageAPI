#!/bin/sh
python manage.py makemigrations --noinput
python manage.py migrate
python manage.py createcachetable
python manage.py shell < "utils/create_superuser.py"
python manage.py runserver 0.0.0.0:8000
