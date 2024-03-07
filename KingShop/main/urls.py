from django.urls import path, re_path
from main.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logo, name='logout'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('category_products/<str:category_name>/', category_products, name='category_products'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('del_from_cart/', del_from_cart, name='del_from_cart'),
    path('cart_up/', cart_up, name='cart_up'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

