"""Test for models"""
import datetime

from django.test import TestCase
from django.utils import timezone

from core import models
from core.models import AccessToken


def create_valid_token():
    """Create a valid token"""
    AccessToken.objects.create(token="valid_token", expires_at=timezone.now() + datetime.timedelta(minutes=5))


def create_expired_token():
    """Create an expired token"""
    AccessToken.objects.create(token="expired_token", expires_at=timezone.now() - datetime.timedelta(minutes=5))


class ModelsTests(TestCase):
    """Test models"""

    def test_create_product(self):
        """Test creating a product"""

        product_description = 'test description'
        product = models.Product.objects.create(name='test product', description=product_description)

        self.assertEqual(product.name, product.name)
        self.assertEqual(product.description, product_description)

    def test_get_valid_token(self):
        """Test that get_valid_token returns the valid token and not the expired one"""

        create_expired_token()
        create_valid_token()

        self.assertEqual(AccessToken.get_valid_token(), "valid_token")

    def test_expired_token(self):
        """Test that an expired token is not returned as a valid token"""

        create_expired_token()
        create_valid_token()

        expired_token = AccessToken.objects.get(token="expired_token")
        self.assertNotEqual(AccessToken.get_valid_token(), expired_token)
