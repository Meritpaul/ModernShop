from django import forms

FC = 'form-control'

class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('cod',   'Cash on Delivery'),
        ('card',  'Credit / Debit Card'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
    ]

    first_name = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': FC, 'placeholder': 'John'}))
    last_name  = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': FC, 'placeholder': 'Doe'}), required=False)
    email      = forms.EmailField(widget=forms.EmailInput(attrs={'class': FC, 'placeholder': 'john@example.com'}))
    phone      = forms.CharField(max_length=20,   widget=forms.TextInput(attrs={'class': FC, 'placeholder': '+880 1800 000000'}))
    address    = forms.CharField(widget=forms.TextInput(attrs={'class': FC, 'placeholder': 'House, Road, Area'}))
    city       = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': FC, 'placeholder': 'Dhaka'}))
    state      = forms.CharField(max_length=100,  required=False, widget=forms.TextInput(attrs={'class': FC, 'placeholder': 'Dhaka Division'}))
    zip_code   = forms.CharField(max_length=20,   required=False, widget=forms.TextInput(attrs={'class': FC, 'placeholder': '1207'}))
    country    = forms.CharField(max_length=100,  initial='Bangladesh', widget=forms.TextInput(attrs={'class': FC}))
    notes      = forms.CharField(required=False,  widget=forms.Textarea(attrs={'class': FC, 'rows': 4, 'placeholder': 'Special delivery instructions...'}))
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect())
