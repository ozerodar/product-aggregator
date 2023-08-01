"""External services utilities and API calls."""

import requests
import json
import os
import datetime

from django.utils import timezone

from core.models import AccessToken


APPLIFTING_API = "https://python.exercise.applifting.cz/api/v1"
APPLIFTING_API_TOKEN = os.getenv('APPLIFTING_API_TOKEN')
URL_TOKEN = f"{APPLIFTING_API}/auth"
URL_REGISTER_PRODUCT = f"{APPLIFTING_API}/products/register"


def get_auth_token() -> str:
    """Retrieve access token from API.

    Sample response:
    {
        "access_token": "string"
    }
    Returns:
        str: access token
    """
    if not APPLIFTING_API_TOKEN:
        raise Exception("APPLIFTING_API_TOKEN environment variable is not set")

    headers = {'Bearer': APPLIFTING_API_TOKEN, 'Content-Type': 'application/json'}

    try:
        response = requests.post(URL_TOKEN, headers=headers)
    except Exception as e:
        print("Failed to get auth token")
    return response.json().get('access_token')


def get_token() -> str:
    """Retrieve access token from database.

    If token is not valid, request new one from API.
    Returns:
        str: access token
    """
    if token := AccessToken.get_valid_token():
        return token
    else:
        new_token = get_auth_token()
        print(f"Access token: {new_token}")
        AccessToken.objects.create(token=new_token, expires_at=timezone.now() + datetime.timedelta(minutes=5))
        return new_token


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
        print(headers)
        print(product_data)
        res = requests.post(URL_REGISTER_PRODUCT, headers=headers, json=product_data)
        res.raise_for_status()
        print(f'Response status code: {res.status_code}')
        print(f'Product registered with id: {res.json()}')
    except Exception as e:
        print(f"Failed to register product: {e}")


if __name__ == "__main__":
    token = get_auth_token()
    print(token)
