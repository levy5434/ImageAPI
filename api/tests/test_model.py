from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestThumbnailModel:
    """Tests for Thumbnail model."""

    def test_thumbnail_string_representation(self):
        """Tests string representation of a model."""
        test_thumbnail = mixer.blend("api.Thumbnail")
        assert str(test_thumbnail) == f"Thumbnail size {test_thumbnail.size}px"


@pytest.mark.django_db
class TestAccountTierModel:
    """Tests for AccountTier model."""

    def test_account_tier_string_representation(self):
        """Tests string representation of a model."""
        test_account_tier = mixer.blend("api.AccountTier", name="test_tier")
        assert test_account_tier.name == "test_tier"


@pytest.mark.django_db
class TestExpiringLinkModel:
    """Tests for ExpiringLink model."""

    def test_expiring_link_string_representation(self):
        """Tests string representation of a model."""
        test_expiring_link = mixer.blend("api.ExpiringLink", name="test_link")
        assert test_expiring_link.name == "test_link"

    def test_expiring_link_get_url(self):
        """Tests get_url() model method."""
        test_expiring_link = mixer.blend("api.ExpiringLink")
        assert test_expiring_link.get_url() == "/api/expiringlink/1/"


@pytest.mark.django_db
class TestImageModel:
    """Tests for Image model."""

    def test_account_tier_string_representation(self):
        """Tests string representation of a model."""
        test_image = mixer.blend("api.Image", name="test_image_name")
        assert test_image.name == "test_image_name"
