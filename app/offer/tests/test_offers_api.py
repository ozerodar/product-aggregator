"""Tests for offer API requests."""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Offer, Product
from offer.serializers import OfferSerializer


OFFERS_URL = reverse('offer:offer-list')


def create_offer(product, **params):
    """Create and return a sample offer"""
    defaults = {
        "id": "6663a9c1-afc1-f54c-be83-69a6f8470c19",
        "price": 444,
        "items_in_stock": 10,
    }

    defaults.update(params)

    return Offer.objects.create(product=product, **defaults)


def create_product(**params):
    """Create and return a sample product"""
    defaults = {
        "name": "Milk",
        "description": "Sample description",
    }
    defaults.update(params)

    return Product.objects.create(**defaults)


class OffersAPITests(TestCase):
    """Test the offer API."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_offers(self):
        """Test retrieving offers."""

        product = create_product()
        create_offer(product, id="33e3a9c1-afc1-f54c-be83-69a6f8470c19", price=444, items_in_stock=4)
        create_offer(product, id="44e3a9c1-afc1-f54c-be83-69a6f8470c19", price=555, items_in_stock=5)

        res = self.client.get(OFFERS_URL)

        offers = Offer.objects.all().order_by("-id")
        serializer = OfferSerializer(offers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
