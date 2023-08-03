"""Serializers for Offer"""

from rest_framework import serializers
from core.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ["product", "price", "items_in_stock"]
