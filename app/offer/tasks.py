import os
import requests

from celery import shared_task

from core.services import get_token
from core.models import Offer, Product

APPLIFTING_API = os.getenv("URL_OFFERS")
URL_OFFERS = f"{APPLIFTING_API}/products/{{product_id}}/offers"


@shared_task
def fetch_offers():
    """Periodic task for fetching orders"""
    token = get_token()
    headers = {"Bearer": token}

    print(f"Fetching offers for {Product.objects.count()} products", flush=True)

    for product in Product.objects.all():
        url = URL_OFFERS.format(product_id=product.id)

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch offers for product {product.id}: {e}")
            continue

        offers_data = response.json()
        print(f"Offers for product {product.name} fetched successfully")

        # Delete existing offers for the product
        product.offers.all().delete()

        # Create new offers based on the response
        for offer_data in offers_data:
            Offer.objects.create(
                id=offer_data["id"],
                price=offer_data["price"],
                items_in_stock=offer_data["items_in_stock"],
                product=product,
            )
