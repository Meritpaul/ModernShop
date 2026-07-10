from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import User, Address

FC = 'form-control'


class RegisterForm(UserCreationForm):
    email     = forms.EmailField(widget=forms.EmailInput(attrs={'class': FC, 'placeholder': 'Email address'}))
    username  = forms.CharField(widget=forms.TextInput(attrs={'class': FC, 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': FC, 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': FC, 'placeholder': 'Confirm password'}))

    class Meta:
        model  = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': FC, 'placeholder': 'Email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': FC, 'placeholder': 'Password'}))


class StyledPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': FC, 'placeholder': 'Email address'}))


class StyledSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': FC, 'placeholder': 'New password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': FC, 'placeholder': 'Confirm new password'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'bio', 'avatar')
        widgets = {
            'username':   forms.TextInput(attrs={'class': FC}),
            'first_name': forms.TextInput(attrs={'class': FC}),
            'last_name':  forms.TextInput(attrs={'class': FC}),
            'phone':      forms.TextInput(attrs={'class': FC}),
            'bio':        forms.Textarea(attrs={'class': FC, 'rows': 3}),
            'avatar':     forms.FileInput(attrs={'class': FC}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model  = Address
        fields = ('full_name', 'phone', 'address_line', 'city', 'state', 'zip_code', 'country', 'is_default')
        widgets = {
            'full_name':    forms.TextInput(attrs={'class': FC}),
            'phone':        forms.TextInput(attrs={'class': FC}),
            'address_line': forms.Textarea(attrs={'class': FC, 'rows': 2}),
            'city':         forms.TextInput(attrs={'class': FC}),
            'state':        forms.TextInput(attrs={'class': FC}),
            'zip_code':     forms.TextInput(attrs={'class': FC}),
            'country':      forms.TextInput(attrs={'class': FC}),
        }
