from api.models import AccountTier
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from mixer.backend.django import mixer
from api.models import User


@pytest.mark.django_db
class TestExpiringLinkViewSet:
    """Test for ExpiringLinkViewSet."""

    client = APIClient()

    def test_get_expiring_link(self):
        """Tests getting an expiring link."""
        expiring_link = mixer.blend("api.ExpiringLink")
        url = reverse("api:expiringlink-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        assert response.data == {"url": expiring_link.url}
        assert response.status_code == 200


@pytest.mark.django_db
class TestImageViewSet:
    """Tests for ImageViewSet."""

    client = APIClient()
    url = "http:test.com/upload/test"
    url_200_px = "http:test.com/upload/w_200,h_200/test"
    url_400_px = "http:test.com/upload/w_400,h_400/test"

    @pytest.fixture
    def dummy_basic_user(self) -> object:
        """Creates dummy user with basic account tier."""
        dummy_thumbnail = mixer.blend("api.Thumbnail")
        dummy_basic_tier = AccountTier.objects.get_or_create(
            name="Basic", original_size=False, fetch_url=False
        )[0]
        dummy_basic_tier.thumbnail_sizes.add(dummy_thumbnail)
        obj = User.objects.get_or_create(
            username="dummy_basic_user",
            password="dummy_password",
            accountTier=dummy_basic_tier,
        )[0]
        return obj

    @pytest.fixture
    def dummy_premium_user(self) -> object:
        """Creates dummy user with basic premium account tier."""
        dummy_thumbnail = mixer.blend("api.Thumbnail", size=200)
        dummy_thumbnail2 = mixer.blend("api.Thumbnail", size=400)
        dummy_premium_tier = AccountTier.objects.get_or_create(
            name="Premium", original_size=True, fetch_url=False
        )[0]
        dummy_premium_tier.thumbnail_sizes.add(dummy_thumbnail)
        dummy_premium_tier.thumbnail_sizes.add(dummy_thumbnail2)
        obj = User.objects.get_or_create(
            username="dummy_premium_user",
            password="dummy_password",
            accountTier=dummy_premium_tier,
        )[0]
        return obj

    @pytest.fixture
    def dummy_enterprise_user(self) -> object:
        """Creates dummy user with enterprise account tier."""
        dummy_thumbnail = mixer.blend("api.Thumbnail", size=200)
        dummy_thumbnail2 = mixer.blend("api.Thumbnail", size=400)
        dummy_enterprise_tier = AccountTier.objects.get_or_create(
            name="Enterprise", original_size=True, fetch_url=True
        )[0]
        dummy_enterprise_tier.thumbnail_sizes.add(dummy_thumbnail)
        dummy_enterprise_tier.thumbnail_sizes.add(dummy_thumbnail2)
        obj = User.objects.get_or_create(
            username="dummy_enterprise_user",
            password="dummy_password",
            accountTier=dummy_enterprise_tier,
        )[0]
        return obj

    def test_get_unauthenticated_call(self):
        """Tests unauthenticated get message call."""
        mixer.blend("api.Image", url=self.url)
        url = reverse("api:image-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        assert (
            response.data["detail"]
            == "Authentication credentials were not provided."  # noqa
        )
        assert response.status_code == 403

    def test_get_image_basic_user(self, dummy_basic_user):
        """Tests getting an image for basic user."""
        self.client.force_authenticate(user=dummy_basic_user)
        image = mixer.blend("api.Image", url=self.url, owner=dummy_basic_user)
        url = reverse("api:image-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.client.force_authenticate(user=None)
        assert response.data == {"name": image.name, "url": self.url}
        assert response.status_code == 200

    def test_get_image_premium_user(self, dummy_premium_user):
        """Tests getting an image for premium user."""
        self.client.force_authenticate(user=dummy_premium_user)
        image = mixer.blend(
            "api.Image", url=self.url, owner=dummy_premium_user
        )
        url = reverse("api:image-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.client.force_authenticate(user=None)
        assert response.data == {
            "name": image.name,
            "url": self.url,
            "Thumbnail 200px": self.url_200_px,
            "Thumbnail 400px": self.url_400_px,
        }
        assert response.status_code == 200

    def test_get_image_enterprise_user(self, dummy_enterprise_user):
        """Tests getting an image for enterprise user."""
        self.client.force_authenticate(user=dummy_enterprise_user)
        image = mixer.blend(
            "api.Image", url=self.url, owner=dummy_enterprise_user
        )
        url = reverse("api:image-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.client.force_authenticate(user=None)
        assert response.data == {
            "name": image.name,
            "url": self.url,
            "Thumbnail 200px": self.url_200_px,
            "Thumbnail 400px": self.url_400_px,
        }
        assert response.status_code == 200
