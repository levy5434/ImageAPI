from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ExpiringLink, Image
from .serializers import (
    ExpiringLinkSerializer,
    ImageLinkSerializer,
    ImageSerializer,
)


class ImageViewSet(viewsets.ModelViewSet):
    """Viewset for Image model."""

    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()
    http_method_names = ["get", "post", "head"]

    def get_queryset(self) -> QuerySet:
        """Returns Image objects of requested user."""
        return Image.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        """Returns serializer based on request user account tier settings."""
        if self.request.user.accountTier.fetch_url:
            return ImageLinkSerializer
        return ImageSerializer


class ExpiringLinkViewSet(viewsets.ViewSet):
    """Viewset for ExpiringLink."""

    def retrieve(self, request, pk: int) -> Response:
        """Checks link expiration time, returns data if it is valid."""
        queryset = ExpiringLink.objects.all()
        expiring_link = get_object_or_404(queryset, pk=pk)
        timezone = pytz.timezone(settings.TIME_ZONE)
        expiration_time = expiring_link.created_time + timedelta(
            seconds=expiring_link.expiration_time
        )
        if (expiration_time) < datetime.now(tz=timezone):
            return Response({"url": "This link has expired!"})
        serializer = ExpiringLinkSerializer(expiring_link)
        return Response(serializer.data)
