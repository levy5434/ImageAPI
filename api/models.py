from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class Thumbnail(models.Model):
    """
    Represents thumbnail size.

    Attributes:
        size (int): Stores Thumbnail size.
    """

    size = models.PositiveIntegerField()

    def __str__(self) -> str:
        """Returns string representation of Thumbnail object."""
        return f"Thumbnail size {self.size}px"


class AccountTier(models.Model):
    """
    Represents account's permissions.

    Attributes:
        name (str): AccountTier's name.
        thumbnail_sizes (QuerySet): Available thumbnail sizes.
        original_size (bool): Permission to store original size Image objects.
        fetch_url (bool): Permission to make ExpiryLink's
    """

    name = models.CharField(max_length=32)
    thumbnail_sizes = models.ManyToManyField(Thumbnail)
    original_size = models.BooleanField()
    fetch_url = models.BooleanField()

    def __str__(self) -> str:
        """Returns string representation of AccountTier object."""
        return f"{self.name}"


class User(AbstractUser):
    """User model extended to have an account tier."""

    accountTier = models.ForeignKey(
        "api.AccountTier", on_delete=models.DO_NOTHING, blank=True, null=True
    )


class Image(models.Model):
    """
    Represents URL to an image and it's owner.

    Attributes:
        owner (object): ForeignKey to User.
        name (str): Name of the image.
        url (str): URL to  the image.
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    name = models.CharField(max_length=256, unique=True)
    url = models.URLField()

    def __str__(self) -> str:
        """Returns string representation of Image object."""
        return f"{self.name}"


class ExpiringLink(models.Model):
    """
    Represents link which expires after given time.

    Attributes:
        url (str): Destination's URL.
        image (object): ForeignKey to image object.
        created_time (object): Creation date and time.
        expiration_time (int): Expiration time of URL in seconds.
    """

    url = models.URLField()
    image = models.ForeignKey(Image, on_delete=CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    expiration_time = models.IntegerField()

    def __str__(self) -> str:
        """Returns string representation of ExpiringLink object."""
        return f"{self.url}"

    def get_url(self) -> str:
        """Returns object's url."""
        return reverse("api:expiringlink-detail", kwargs={"pk": self.pk})
