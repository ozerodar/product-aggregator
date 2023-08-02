import requests

from celery import shared_task

from core.services import get_token
from core.models import Offer, Product

APPLIFTING_API = "https://python.exercise.applifting.cz/api/v1"
URL_OFFERS = f"{APPLIFTING_API}/products/{{product_id}}/offers"


@shared_task
def fetch_offers():
    """Periodic task for fetching orders"""
    token = get_token()
    headers = {'Bearer': token}

    print('Fetching offers...')

    for product in Product.objects.all():
        url = URL_OFFERS.format(product_id=product.id)
        print(f"url: {url}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch offers for product {product.id}: {e}")
            continue

        offers_data = response.json()
        print(f"Offers for product {product.id} fetched successfully")
        print(offers_data)

        # Delete existing offers for the product
        product.offers.all().delete()

        # Create new offers based on the response
        for offer_data in offers_data:

            print('offer data: ', offer_data)

            Offer.objects.create(
                id=offer_data['id'],
                price=offer_data['price'],
                items_in_stock=offer_data['items_in_stock'],
                product=product,
            )

@shared_task
def add(x, y):
    # Celery recognizes this as the `movies.tasks.add` task
    # the name is purposefully omitted here.
    return x + y
