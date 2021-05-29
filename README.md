# ImageAPI

Application lets users upload their JPG or PNG image files to Cloudinary cloud and stores urls to them. You can create account tiers with permissions which allows users to upload original size images or thumbnails, which size can be set via administration panel. Another ability which can be set to an account tier is fetching expiring link to an image which can last from 300 seconds to 30000 seconds. Users can use POST request to send images and GET request  to retrieve urls to all of theirs uploaded files or get a single image url.


## Table of contents
* [Technologies](#technologies)
* [Initialize .env](#initialize)
* [Docker-compose](#docker-compose)
* [Setup](#setup)

## Technologies
* Python version: 3.9.5
* Django version: 3.2.3
* DRF version: 3.12.4

## Initialize

Create .env file with enviromental variables in project's base folder with application secret key, cloudinary authentication and superuser credentials:
```
SECRET_KEY = <project_secret_key>
CLOUD_NAME = <cloudinary_cloud_name>
API_KEY = <cloudinary_api_key>
API_SECRET = <cloudinary_api_secret>

DJANGO_SUPERUSER_USERNAME = <superuser_username>
DJANGO_SUPERUSER_PASSWORD = <superuser_password>
DJANGO_SUPERUSER_EMAIL = <superuser_email>
```

## Docker-compose

Project is docker-compose ready to run it type:
```
$ docker-compose up
```
Server will be running on http://localhost:8000/

## Setup

Create and run an isolated environment:
```
$ python -m venv env
$ source env/bin/activate
```

Install the dependencies:
```
(env)$ pip install -r requirements.txt
```

Makemigrations and migrate:
```
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```
If DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD was set in .env file you can create superuser by using:
```
(env)$ python manage.py shell < "utils/create_superuser.py"
```

Or:
```
(env)$ python manage.py createsuperuser
```

To run the server:
```
(env)$ python manage.py runserver
```
