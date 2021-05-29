import cloudinary.uploader
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from rest_framework import serializers

from .models import ExpiringLink, Image, User


class ExpiringLinkSerializer(serializers.Serializer):
    """
    Serializer for ExpiringLink.

    Args:
        url(str): Destination URL.
    """

    url = serializers.URLField()


class ImageSerializer(serializers.ModelSerializer):
    """Image model serializer for AccountTier's with fetch_url==False.

    Args:
        image(file): Passes image file to serializer.
    """

    image = serializers.ImageField(
        allow_empty_file=False,
        write_only=True,
        validators=[FileExtensionValidator(["jpg", "png"])],
    )

    class Meta:
        """Serializer based on Image model."""

        model = Image
        fields = ["name", "url", "image"]
        extra_kwargs = {
            "url": {"read_only": True},
        }

    def to_representation(self, instance: object) -> dict:
        """
        Adds extra thumbnail sizes for users with appropriate
        account tier permits.

        Args:
            instance(object): Image object to serialize.

        Returns:
            dict: Serialized data.
        """
        ret = super(ImageSerializer, self).to_representation(instance)
        user = User.objects.get(id=self.context["request"].user.id)
        if user.accountTier.name != "Basic":
            thumbnails = user.accountTier.thumbnail_sizes.all()
            for thumbnail in thumbnails:
                size = thumbnail.size
                name = f"Thumbnail {size}px"
                first_url_part = ret["url"].split("upload/", 1)[0]
                thumbnail_size = f"upload/w_{size},h_{size}/"
                second_url_part = ret["url"].split("upload/", 1)[1]
                url = first_url_part + thumbnail_size + second_url_part
                extra_ret = {name: url}
                ret.update(extra_ret)
        return ret

    def create(self, validated_data: dict) -> object or None:
        """
        Creates Image object, checks user's account tier permissions
        to upload original size image file or thumbnail.

        Args:
            validated_data(dict): Data to serialize.

        Returns:
            object: Image object or None.
        """
        if not self.is_valid():
            return None
        user = User.objects.get(id=self.context["request"].user.id)
        if user.accountTier.original_size:
            output = cloudinary.uploader.upload(
                self.context["request"].FILES["image"],
                folder=user.username,
                public_id=self.validated_data["name"],
                overwrite=True,
            )
        else:
            output = cloudinary.uploader.upload(
                self.context["request"].FILES["image"],
                folder=user.username,
                public_id=self.validated_data["name"],
                height=200,
                width=200,
                crop="scale",
                overwrite=True,
            )
        new_image = Image(
            name=self.validated_data["name"], owner=user, url=output["url"]
        )
        new_image.save()
        return new_image


class ImageLinkSerializer(serializers.ModelSerializer):
    """
    Image model serializer for AccountTier's with fetch_url==True.

    Args:
        image(file): Passes image file to serializer.
        link_expiry_time(int): Optional; If passed creates expiring link
                     to image which expires after given value in seconds.
    """

    image = serializers.ImageField(
        allow_empty_file=False,
        write_only=True,
        validators=[FileExtensionValidator(["jpg", "png"])],
    )
    link_expiry_time = serializers.IntegerField(
        required=False,
        write_only=True,
        validators=[MaxValueValidator(30000), MinValueValidator(300)],
    )

    class Meta:
        """Serializer based on Image model."""

        model = Image
        fields = ["name", "url", "image", "link_expiry_time"]
        extra_kwargs = {
            "url": {"read_only": True},
        }

    def to_representation(self, instance: object) -> dict:
        """
        Adds extra thumbnail sizes for users with appropriate
        account tier permits and attached expiring link if it was created.

        Args:
            instance(object): Image object to serialize.

        Returns:
            dict: Serialized data.
        """
        ret = super(ImageLinkSerializer, self).to_representation(instance)
        user = User.objects.get(id=self.context["request"].user.id)
        if user.accountTier.name != "Basic":
            thumbnails = user.accountTier.thumbnail_sizes.all()
            for thumbnail in thumbnails:
                size = thumbnail.size
                name = f"Thumbnail {size}px"
                first_url_part = ret["url"].split("upload/", 1)[0]
                thumbnail_size = f"upload/w_{size},h_{size}/"
                second_url_part = ret["url"].split("upload/", 1)[1]
                url = first_url_part + thumbnail_size + second_url_part
                extra_ret = {name: url}
                ret.update(extra_ret)
        try:
            expiring_link = ExpiringLink.objects.get(url=ret["url"])
            expiring_link_url = (
                self.context["request"].build_absolute_uri("/")[:-1]
                + expiring_link.get_url()  # noqa
            )
            extra_ret = {"Expiring link": expiring_link_url}
            ret.update(extra_ret)
        except:  # noqa
            pass
        return ret

    def create(self, validated_data: dict) -> object or None:
        """
        Creates Image object, checks user's account tier permissions to upload
        original size image file or thumbnail.
        Creates expiring link if variable link_expiry_time is passed.

        Args:
            validated_data(dict): Image object data.

        Returns:
            object: Image object or None.
        """
        if not self.is_valid():
            return None
        user = User.objects.get(id=self.context["request"].user.id)
        if user.accountTier.original_size:
            output = cloudinary.uploader.upload(
                self.context["request"].FILES["image"],
                folder=user.username,
                public_id=self.validated_data["name"],
                overwrite=True,
            )
        else:
            output = cloudinary.uploader.upload(
                self.context["request"].FILES["image"],
                folder=user.username,
                public_id=self.validated_data["name"],
                height=200,
                width=200,
                crop="scale",
                overwrite=True,
            )
        new_image = Image(
            name=self.validated_data["name"], owner=user, url=output["url"]
        )
        new_image.save()
        try:
            expiring_link = ExpiringLink(
                image=new_image,
                url=new_image.url,
                expiration_time=self.validated_data["link_expiry_time"],
            )
            expiring_link.save()
        except:  # noqa
            pass
        return new_image
