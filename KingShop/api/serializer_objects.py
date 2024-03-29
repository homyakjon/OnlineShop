from main.models import Category, Order, User, UserProfile
from api.serializers import UserSerializer, ProductSerializer, OrderSerializer, NewOrderSerializer,\
    SaveUserProductSerializer

# Оголошуємо змінну instance на рівні модуля
instance = None


def create_objects():
    global instance
    user_data = {
        'username': 'Korol05 Yura',
        'email': 'eddy@example.com',
        'first_name': 'Freddy',
        'last_name': 'Van',
    }

    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        instance = user_serializer.save()
        profile = UserProfile.objects.create(user=instance, balance=500)
        print("User created:", instance)
        print("User balance:", profile.balance)
    else:
        print("Error creating user:", user_serializer.errors)

    category = Category.objects.create(name='Audi', description='Q7')

    product_data = {
        'name': 'Samsung Galaxy S-24',
        'description': "Hello, New Smart Phone",
        'price': 650,
        'categories': [category.id]
    }
    product_serializer = ProductSerializer(data=product_data)
    if product_serializer.is_valid():
        product_instance = product_serializer.save()
        print("Product created:", product_serializer.data)
    else:
        print("Error creating product:", product_serializer.errors)

    order_data = {'user': instance.id, 'items': [instance.id]}
    order_serializer = OrderSerializer(data=order_data)
    if order_serializer.is_valid():
        order_instance = order_serializer.save()
        print("Order created:", order_serializer.data)
    else:
        print("Error creating order:", order_serializer.errors)

    order = Order.objects.first()
    serializer = NewOrderSerializer(order)
    data = serializer.data
    print('Result:', data)

    save_user_product_serializer = SaveUserProductSerializer(instance=instance)
    serialized_data = save_user_product_serializer.data
    print('User and purchases:', serialized_data)

    user_instance = User.objects.get(pk=3)
    serializer = UserSerializer(user_instance)
    print(serializer.data)
