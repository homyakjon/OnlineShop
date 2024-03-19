from django.urls import path, re_path
from api.views import *


urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:amount>/', UserListView.as_view(), name='user_list_with_amount'),
    path('users/<int:pk>/orders/', UserListView.as_view(), name='user_orders'),
    path('users/<int:pk>/', UserRetrieveView.as_view(), name='user_detail'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/<slug:name>/', ProductListView.as_view(), name='products_name'),
    path('products/<int:pk>/', ProductRetrieveView.as_view(), name='products_detail'),
    path('products/create/', ProductCreateView.as_view(), name='products_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='products_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='products_delete'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderRetrieveView.as_view(), name='orders_detail'),
    path('orders/create/', OrderCreateView.as_view(), name='orders_create'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='orders_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='orders_delete'),
]



