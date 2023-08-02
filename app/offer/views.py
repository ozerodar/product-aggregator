"""Views for the offer APIs"""
from rest_framework import viewsets

from core.models import Offer
from offer import serializers


class OfferViewSet(viewsets.ModelViewSet):
    """View for manage offers APIs"""

    serializer_class = serializers.OfferSerializer
    queryset = Offer.objects.all()

    def get_queryset(self):
        """Retrieve offers"""
        return self.queryset.order_by("-id")
