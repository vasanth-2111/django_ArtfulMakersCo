from django import forms
from django.contrib.auth.models import User
from .models import Artisan, Customer, Product
from django import forms

class ArtisanUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class ArtisanForm(forms.ModelForm):
    class Meta:
        model = Artisan
        fields = ['bio', 'profile_picture', 'address']


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_picture']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']


class ArtisanLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
