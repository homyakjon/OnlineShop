from rest_framework import viewsets
from rest_framework.response import Response
from main.models import User, Product, Order
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from rest_framework.decorators import action
from rest_framework import filters


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def get_queryset(self):
        amount = self.request.query_params.get('amount')
        if amount:
            try:
                amount = float(amount)
                queryset = User.objects.filter(userprofile__balance__gte=amount)
                return queryset
            except ValueError:
                pass
        return User.objects.all()

    @action(methods=['get'], detail=True)
    def orders(self, request, pk=None):
        user = self.get_object()
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
            return queryset
        else:
            return queryset.none()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

