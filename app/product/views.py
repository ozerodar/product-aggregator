"""Views for the products APIs"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Offer, Product
from offer.serializers import OfferSerializer
from product import serializers
from product.services import register_product


class ProductViewSet(viewsets.ModelViewSet):
    """View for manage product APIs"""

    serializer_class = serializers.ProductDetailSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        """Retrieve the products"""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.ProductSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Override perform_create to register product at external server"""
        serializer.save()  # Save the product in the db
        register_product(serializer.data)  # Register it on the external server

    @action(detail=False, methods=['delete'], url_path='')
    def delete_all(self, request):
        """Delete all products"""
        Product.objects.all().delete()
        return Response({'status': 'All Products Deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='offers')
    def get_offers(self, request, pk):
        """Get the offers from the external server"""
        offers = Offer.objects.filter(product_id=pk)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='offers')
    def get_all_offers(self, request):
        """Get the offers from the external server"""
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
