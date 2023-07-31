"""Test for models"""

from django.db import IntegrityError
from django.test import TestCase

from core import models

class ModelsTests(TestCase):
    """Test models"""

    def test_create_product(self):
        """Test creating a product"""

        product_description = 'test description'
        product = models.Product.objects.create(name='test product', description=product_description)

        self.assertEqual(product.name, product.name)
        self.assertEqual(product.description, product_description)
