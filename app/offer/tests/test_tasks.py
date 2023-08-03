from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Product
from offer.tasks import fetch_offers


class FetchOffersTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="user@example.com", password="pass123")

    @patch("requests.get")
    @patch("offer.tasks.get_token")
    def test_fetch_offers(self, mock_get_token, mock_get):
        product = Product.objects.create(user=self.user, name="Product 1", id="11e3a9c1-afc1-f54c-be83-69a6f8470c19")

        mock_get_token.return_value = "fake_token"

        mock_response = [
            {"id": "e039c854-becb-f869-1348-6f34988207a5", "items_in_stock": 10, "price": 100},
            {"id": "89e3a9c1-afc1-f54c-be83-69a6f8470c19", "items_in_stock": 20, "price": 200},
        ]
        mock_get.return_value.json.return_value = mock_response

        fetch_offers()

        self.assertEqual(mock_get.call_count, 1)

        product.refresh_from_db()

        print("very products", product.offers.all())
        self.assertEqual(product.offers.count(), 2)
        for i, offer in enumerate(product.offers.all().order_by("-id")):
            self.assertEqual(offer.items_in_stock, mock_response[i]["items_in_stock"])
            self.assertEqual(offer.price, mock_response[i]["price"])
