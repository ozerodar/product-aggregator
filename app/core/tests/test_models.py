"""Test for models"""
import datetime

from django.contrib.auth import get_user_model
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
        user = get_user_model().objects.create_user("test@example.com", "pass123")
        new_product = models.Product.objects.create(user=user, name='test product', description=product_description)

        product = models.Product.objects.get(id=new_product.id)
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(product.description, product_description)

    def test_create_offer(self):
        """Test creating an offer"""

        user = get_user_model().objects.create_user("test@example.com", "pass123")
        product = models.Product.objects.create(user=user, name='test product', description='Something')
        new_offer = models.Offer.objects.create(product=product, price=10, items_in_stock=10)

        offer = models.Offer.objects.get(id=new_offer.id)
        self.assertEqual(new_offer.product.id, product.id)
        self.assertEqual(new_offer.price, offer.price)
        self.assertEqual(new_offer.items_in_stock, offer.items_in_stock)

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
