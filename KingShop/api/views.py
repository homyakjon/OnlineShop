from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from main.models import User, Product, Order
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from threading import Timer
from rest_framework.filters import SearchFilter, OrderingFilter


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
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'price']


class AuthView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @permission_classes([IsAuthenticatedOrReadOnly])
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'message': 'Authentication successful', 'user': username})


class TokenView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

            t = Timer(600, self.invalidate_token, args=[token])
            t.start()

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })

    def invalidate_token(self, token):
        token.delete()
        print("The token has been revoked: None")




