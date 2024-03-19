from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from main.models import User, Product, Order
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from rest_framework.decorators import action


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        amount = self.kwargs.get('amount')
        if amount:
            try:
                amount = float(amount)
                queryset = User.objects.filter(userprofile__balance__gte=amount)
                return queryset
            except ValueError:
                pass
        else:
            queryset = User.objects.all()
            return queryset

    @action(methods=['get'], detail=True)
    def orders(self, request, pk):
        user = User.objects.get(pk=pk)
        orders = Order.objects.filter(user=user)
        order_ids = [order.id for order in orders]
        return Response({'user': user.id, 'orders': order_ids})


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self, filter=None):
        name = self.kwargs.get('name')
        if name is not filter:
            queryset = Product.objects.filter(name__icontains=name)
            return queryset
        queryset = Product.objects.all()
        return queryset


class ProductRetrieveView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListView(ListAPIView):

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class OrderRetrieveView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderUpdateView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDeleteView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


