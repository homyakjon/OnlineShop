from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Product, Order, ReturnProduct


class UserSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, source='userprofile.balance', read_only=True)
    orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='order_set')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'amount', 'balance', 'orders']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['orders'] = [order.id for order in instance.order_set.all()]
        return representation


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'categories']

    def create(self, validated_data):
        if 'name' in validated_data:
            validated_data['name'] += '!'
        return super().create(validated_data)


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


class ReturnProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnProduct
        fields = ['name', 'description', 'price']


























