"""Database models."""
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        "Create, save and return new user"
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Product(models.Model):
    """Product model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1000, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Offer(models.Model):
    """Offer model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers")
    price = models.PositiveIntegerField()
    items_in_stock = models.PositiveIntegerField()


class AccessToken(models.Model):
    """Access token model"""

    token = models.CharField(max_length=200, editable=False)
    expires_at = models.DateTimeField()

    @classmethod
    def get_valid_token(cls):
        try:
            token_obj = cls.objects.filter(expires_at__gt=timezone.now())
            if token_obj:
                return token_obj[0].token
        except cls.DoesNotExist:
            return None
