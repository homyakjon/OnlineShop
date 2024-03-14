from main.models import Category, Order, User, Product
from api.serializers import UserSerializer, ProductSerializer, OrderSerializer, NewOrderSerializer,\
    SaveUserProductSerializer
from rest_framework.renderers import JSONRenderer


def create_objects():
    user_data = {'username': 'Yurii34', 'email': 'eddy@example.com', 'first_name': 'Freddy', 'last_name': 'Van'}
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user_instance = user_serializer.save()
        print("User created:", JSONRenderer().render(user_serializer.data))
    else:
        print("Error creating user:", user_serializer.errors)

    category = Category.objects.create(name='New_Category', description='This category about rock-group')

    product_data = {
        'name': 'Van Halen',
        'description': "the band's 1978 debut album, heralded the arrival of a hard rock",
        'price': 99.99,
        'categories': [category.id]
    }
    product_serializer = ProductSerializer(data=product_data)
    if product_serializer.is_valid():
        product_instance = product_serializer.save()
        print("Product created:", JSONRenderer().render(product_serializer.data))
    else:
        print("Error creating product:", product_serializer.errors)

    order_data = {'user': user_instance.id, 'items': [product_instance.id]}
    order_serializer = OrderSerializer(data=order_data)
    if order_serializer.is_valid():
        order_instance = order_serializer.save()
        print("Order created:", JSONRenderer().render(order_serializer.data))
    else:
        print("Error creating order:", order_serializer.errors)

    order = Order.objects.first()
    serialiser = NewOrderSerializer(order)
    data = serialiser.data
    print('Result:', data)

    save_user_product_serializer = SaveUserProductSerializer(instance=user_instance)

    serialized_data = save_user_product_serializer.data
    print('User and purchases:', JSONRenderer().render(serialized_data))


create_objects()

