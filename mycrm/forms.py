from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Record


class SignUpForm(UserCreationForm):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email Address", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('name', 'email', 'username', 'password1', 'password2')


# Define a dictionary of common attributes for the fields
common_attrs = {
    'class': 'form-control',
    'required': False,
}


class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs=common_attrs))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs=common_attrs))
    email = forms.CharField(label="Email Address", widget=forms.TextInput(attrs=common_attrs))
    phone = forms.CharField(label="Phone Number", widget=forms.NumberInput(attrs=common_attrs))
    city = forms.CharField(label="City", widget=forms.TextInput(attrs=common_attrs))
    state = forms.CharField(label="State", widget=forms.TextInput(attrs=common_attrs))

    class Meta:
        model = Record
        fields = "__all__"
