"""Tests for products"""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from core.models import Product
from product.serializers import ProductSerializer, ProductDetailSerializer
from rest_framework import status


URL_PRODUCT_LIST = reverse('product:product-list')
get_url_product_detail = lambda product_id: reverse('product:product-detail', args=[product_id])


def create_product(user, name='Test product', description='Test description'):
    """Create a product"""
    return Product.objects.create(user=user, name=name, description=description)


def create_user(**params):
    """Create and and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicProductTest(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="pass123")
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving products"""

        create_product(user=self.user)
        create_product(user=self.user)

        res = self.client.get(URL_PRODUCT_LIST)

        serializer = ProductSerializer(Product.objects.all().order_by("-id"), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_product_detail(self):
        """Test retrieving product detail"""

        product = create_product(user=self.user)

        url = get_url_product_detail(product_id=product.id)
        res = self.client.get(url)

        serializer = ProductDetailSerializer(product)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    @patch('requests.post')  # This mocks 'requests.post'
    @patch('product.services.get_token')  # This mocks 'requests.post'
    def test_create_product(self, mock_register, mock_token):
        """Test creating a product"""

        payload = {'name': 'New product', 'description': 'Some description'}
        res = self.client.post(URL_PRODUCT_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(product, key))

    def test_partial_update_product(self):
        """Test updating some attributes of a product"""

        original_description = 'Original description'
        product = create_product(user=self.user, description=original_description)
        payload = {'name': 'New name'}

        url = get_url_product_detail(product_id=product.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, payload['name'])
        self.assertEqual(product.description, original_description)

    def test_full_update_product(self):
        """Test updating a product"""

        original_description = 'Original description'
        product = create_product(user=self.user, description=original_description)
        payload = {'name': 'New name', 'description': 'New description'}

        url = get_url_product_detail(product_id=product.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)

    def test_delete_product(self):
        """Test deleting a product"""

        product = create_product(user=self.user)

        url = get_url_product_detail(product_id=product.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product.id).exists())
