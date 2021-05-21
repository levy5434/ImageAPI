"""Stores urls"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"image", views.ImageViewSet, basename="image")
router.register(
    r"expiringlink", views.ExpiringLinkViewSet, basename="expiringlink"
)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
]
