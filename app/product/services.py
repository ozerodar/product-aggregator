"""External services utilities and API calls."""

import requests
import os

from core.services import get_token


APPLIFTING_API = "https://python.exercise.applifting.cz/api/v1"
URL_REGISTER_PRODUCT = f"{APPLIFTING_API}/products/register"


def register_product(product_data):
    """Register product at external server

    Sample response:
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }
    """
    token = get_token()
    headers = {
        'Bearer': token,
        'Content-Type': 'application/json',
    }

    try:
        res = requests.post(URL_REGISTER_PRODUCT, headers=headers, json=product_data)
        res.raise_for_status()
        print(f'Product registered successfully')
    except Exception as e:
        print(f"Failed to register product: {e}")
