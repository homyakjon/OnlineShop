from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProductViewSet, OrderViewSet, AuthView, TokenView


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', AuthView.as_view(), name='auth'),
    path('token/', TokenView.as_view(), name='token'),

]



