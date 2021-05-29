import os
from api.models import User
from django.db import IntegrityError

DJANGO_SUPERUSER_USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME")
DJANGO_SUPERUSER_EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL")
DJANGO_SUPERUSER_PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

try:
    superuser = User.objects.create_superuser(
        username=DJANGO_SUPERUSER_USERNAME,
        email=DJANGO_SUPERUSER_EMAIL,
        password=DJANGO_SUPERUSER_PASSWORD,
    )
    superuser.save()
except IntegrityError:
    print(
        f"Super User with username {DJANGO_SUPERUSER_USERNAME} is already present"
    )
except Exception as e:
    print(e)
