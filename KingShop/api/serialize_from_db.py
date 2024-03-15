from django.http import JsonResponse
from api.serializers import UserSerializer, OrderSerializer, ProductSerializer
from main.models import User, Order, Product


def serialize_from_db():
    user_instance = User.objects.all()
    user_serializer = UserSerializer(user_instance, many=True)
    user_data = user_serializer.data
    print("Serialized User data:", user_data)

    product_instance = Product.objects.all()
    product_serializer = ProductSerializer(product_instance, many=True)
    product_data = product_serializer.data
    print("Serialized Product data:", product_data)

    order_instance = Order.objects.all()
    order_serializer = OrderSerializer(order_instance, many=True)
    order_data = order_serializer.data
    print("Serialized Order data:", order_data)

    return JsonResponse({
        'user_data': user_data,
        'product_data': product_data,
        'order_data': order_data
    })


serialize_from_db()

# exec(open('api/serialize_from_db.py').read())
# exec(open('api/serializer_objects.py').read())