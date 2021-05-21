from api.serializers import (
    ExpiringLinkSerializer,
    ImageSerializer,
    ImageLinkSerializer,
)


def dedent(blocktext):
    return "\n".join([line[12:] for line in blocktext.splitlines()[1:-1]])


class TestExpiringLinkSerializer:
    """Tests ExpiringLinkSerializer."""

    expiring_link_serializer = ExpiringLinkSerializer

    def test_valid_data(self):
        """Tests serializer when valid data is passed."""
        serializer = self.expiring_link_serializer(
            data={"url": "http://test.com"}
        )
        assert serializer.is_valid()
        assert serializer.validated_data == {"url": "http://test.com"}
        assert serializer.errors == {}

    def test_invalid_data(self):
        """Tests invalid data."""
        serializer = self.expiring_link_serializer(data={"url": "test"})
        assert not serializer.is_valid()
        assert serializer.data == {"url": "test"}
        assert serializer.errors == {"url": ["Enter a valid URL."]}

    def test_invalid_field(self):
        """Tests invalid field sent to serializer."""
        serializer = self.expiring_link_serializer(
            data={"test": "http://test.com"}
        )
        assert not serializer.is_valid()
        assert serializer.data == {}
        assert serializer.errors == {"url": ["This field is required."]}

    def test_empty_url_address(self):
        """Tests empty url address."""
        serializer = self.expiring_link_serializer(data={"url": ""})
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.data == {"url": ""}
        assert serializer.errors == {"url": ["This field may not be blank."]}

    def test_validate_none_data(self):
        """Tests serializer when no data is sent."""
        data = None
        serializer = self.expiring_link_serializer(data=data)
        assert not serializer.is_valid()
        assert serializer.errors == {"non_field_errors": ["No data provided"]}


class TestImageSerializer:
    """Tests ImageSerializer."""

    image_serializer = ImageSerializer

    def test_regular_fields(self):
        """Model fields should map to their equivalent serializer fields."""
        expected = dedent(
            """
            ImageSerializer():
                name = CharField(max_length=256, validators=[<UniqueValidator(queryset=Image.objects.all())>])
                url = URLField(read_only=True)
                image = ImageField(allow_empty_file=False, validators=[<django.core.validators.FileExtensionValidator object>], write_only=True)
            """
        )
        assert repr(ImageSerializer()) == expected


class TestImageLinkSerializer:
    """Tests ImageSerializer."""

    image_link_serializer = ImageLinkSerializer

    def test_regular_fields(self):
        """Model fields should map to their equivalent serializer fields."""
        expected = dedent(
            """
            ImageLinkSerializer():
                name = CharField(max_length=256, validators=[<UniqueValidator(queryset=Image.objects.all())>])
                url = URLField(read_only=True)
                image = ImageField(allow_empty_file=False, validators=[<django.core.validators.FileExtensionValidator object>], write_only=True)
                link_expiry_time = IntegerField(required=False, validators=[<django.core.validators.MaxValueValidator object>, <django.core.validators.MinValueValidator object>], write_only=True) 
            """
        )
        assert repr(ImageLinkSerializer()) == expected
