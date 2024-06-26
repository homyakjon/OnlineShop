from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from main.forms import UserRegisterForm, UserLoginForm, AddToCartForm, CategoryForm, ProductForm
from main.models import Product, Category, UserProfile


@login_required
def index(request):
    cart_count = get_cart_count(request)
    user = request.user
    user_balance = user.userprofile.balance if user.is_authenticated else 0
    return render(request, 'index.html', {'cart_count': cart_count, 'balance': user_balance})


def register(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        form.save(request)
        msg = 'Hi, you have successfully registered'
        messages.success(request, msg)
        return redirect('login')
    else:
        form = UserRegisterForm()
        cart_count = get_cart_count(request)
    return render(request, 'register.html', {'form': form, 'cart_count': cart_count})


def login_view(request):
    form = UserLoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)
        msg = 'You have successfully entered the store'
        messages.success(request, msg)
        return redirect('index')
    return render(request, 'login.html', {'form': form})


def logo(request):
    logout(request)
    return redirect('index')


def about(request):
    cart_count = get_cart_count(request)
    return render(request, 'about.html', {'cart_count': cart_count})


def product_list(request):
    return render(request, 'product.html')


def contact(request):
    title = 'Contacts'
    cart_count = get_cart_count(request)
    return render(request, 'contact.html', {'title': title, 'cart_count': cart_count})


def category_products(request, category_name):
    try:
        category = Category.objects.get(name=category_name)
        products = category.product_set.all()
    except Category.DoesNotExist:
        category = None
        products = None

    cart_count = get_cart_count(request)

    return render(request, 'category_products.html', {'category': category,
                                                      'products': products, 'cart_count': cart_count}
                  )


def add_new_category(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Category added successfully.")
        return redirect('add_product')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})


@login_required
def add_new_product(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Item added successfully.")
        return redirect('cart')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


class CartView(View):

    def get(self, request):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart.keys())
        cart_count = get_cart_count(request)
        return render(request, 'cart.html', {'products': products, 'cart': cart, 'cart_count': cart_count})


def add_to_cart(request):
    form = AddToCartForm(request.POST)
    if form.is_valid():
        product_id = form.cleaned_data['product_id']
        product = Product.objects.get(id=product_id)
        if product.price > 0:
            cart = request.session.get('cart', {})
            cart[product_id] = cart.get(product_id, 0) + 1
            request.session['cart'] = cart
            messages.success(request, "Product added to cart")
        else:
            return redirect('error')
        return redirect('cart')
    return redirect('index')


def del_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            messages.success(request, "Product removed successfully.")
            return redirect('cart_up')
        else:
            messages.error(request, "Product does not exist in the cart.")
    return redirect('index')


def get_cart_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values()) if cart else 0
    return total_items


def cart_up(request):
    cart_count = get_cart_count(request)
    cart_ids = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart_ids.keys())
    return render(request, 'cart.html', {'products': products, 'cart_count': cart_count})


def make_order(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    total_price = sum(product.price * cart[str(product.id)] for product in products)

    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if user_profile.balance >= total_price:
        user_profile.balance -= total_price
        user_profile.save()
        request.session['cart'] = {}
        return render(request, 'make_order.html')
    else:
        return render(request, 'error.html', {'error_message': 'Insufficient funds'})


def error_message(request):
    err = 'Price product cannot be negative!'
    return render(request, 'error.html', {'err': err})


