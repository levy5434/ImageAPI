# ImageAPI

Application lets users upload their JPG or PNG image files to Cloudinary cloud and stores urls to them. You can create account tiers with permissions which allows users to upload original size images or thumbnails, which size can be set via administration panel. Another ability which can be set to an account tier is fetching expiring link to an image which can last from 300 seconds to 30000 seconds. Users can use POST request to send images and GET request  to retrieve urls to all of theirs uploaded files or get a single image url.


## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)

## Technologies
* Python version: 3.9.5
* Django version: 3.2.3
* DRF version: 3.12.4

## Setup

Create .env file in project's base folder with application secret key and cloudinary authentication.
```
SECRET_KEY = <project_secret_key>
CLOUD_NAME = <cloudinary_cloud_name>
API_KEY = <cloudinary_api_key>
API_SECRET = <cloudinary_api_secret>
```

Create and run an isolated environment
```
$ python -m venv env
$ source env/bin/activate
```

Install the dependencies:
```
(env)$ pip install -r requirements.txt
```

Migrate and create superuser
```
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py createsuperuser
```

Run the server
```
(env)$ python manage.py runserver
```
