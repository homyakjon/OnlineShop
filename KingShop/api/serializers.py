from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Product, Order


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'categories']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class NewOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    items = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = Order
        fields = '__all__'


class SaveUserProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'product']





























