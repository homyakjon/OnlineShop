from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from main.models import UserProfile, Product


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, request, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, balance=1500)
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None or not user.is_active:
                raise forms.ValidationError("Invalid username or password")

        return cleaned_data


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)

    def add_id(self):
        product_id = self.cleaned_data['product_id']
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise forms.ValidationError("Product does not exist.")
        return product_id


class DelCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_product_id(self):
        product_id = self.cleaned_data['product_id']
        if not Product.objects.filter(id=product_id).exists():
            raise forms.ValidationError("No product with this ID in the cart.")
        return product_id


