from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import RegisterForm, LoginForm, ProfileForm, AddressForm
from .models import Address


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Account created! Welcome to {settings.SITE_NAME}.')
        return redirect('core:home')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.username}!')
        return redirect(request.GET.get('next', '/'))
    if request.method == 'POST':
        messages.error(request, 'Invalid email or password.')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:home')


@login_required
def profile_view(request):
    from orders.models import Order
    orders    = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    addresses = request.user.addresses.all()
    return render(request, 'users/profile.html', {'orders': orders, 'addresses': addresses})


@login_required
def edit_profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated.')
        return redirect('users:profile')
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def add_address_view(request):
    form = AddressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        addr = form.save(commit=False)
        addr.user = request.user
        addr.save()
        messages.success(request, 'Address saved.')
        return redirect('users:profile')
    return render(request, 'users/address_form.html', {'form': form, 'title': 'Add Address'})


@login_required
def delete_address_view(request, pk):
    get_object_or_404(Address, pk=pk, user=request.user).delete()
    messages.success(request, 'Address deleted.')
    return redirect('users:profile')
