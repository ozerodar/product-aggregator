"""Database models."""
import datetime
import uuid

from django.db import models
from django.utils import timezone


class Product(models.Model):
    """Product model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1000, blank=True)


class AccessToken(models.Model):
    """Access token model"""

    token = models.CharField(max_length=200, editable=False)
    expires_at = models.DateTimeField()

    @classmethod
    def get_valid_token(cls):
        try:
            token_obj = cls.objects.get(expires_at__gt=timezone.now())
            return token_obj.token
        except cls.DoesNotExist:
            return None
