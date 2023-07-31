"""Database models."""
import uuid

from django.db import models

class Product(models.Model):
    """Product model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1000, blank=True)
