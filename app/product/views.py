"""Views for the products APIs"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Product
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
