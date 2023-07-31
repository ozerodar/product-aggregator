"""Serializers for product APIs"""

from rest_framework import serializers

from core.models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product objects"""

    class Meta:
        model = Product
        fields = ('id', 'name')
        read_only_fields = ('id',)

class ProductDetailSerializer(ProductSerializer):
    """Serialize a product detail"""

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ('description', )
