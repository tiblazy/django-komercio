from django.core.validators import MinValueValidator

from rest_framework import serializers

from accounts.serializers import AccountSerializer

from .models import Product


class ProductDetailsSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)    
    
    class Meta:
        model = Product
        fields = '__all__'

class ProductBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['id',]