from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from products.models import Product, Coupon
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm


def _safe_next(request, fallback='orders:cart'):
    next_url = request.POST.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return next_url
    return fallback


# ─── Cart helpers ─────────────────────────────────────────────────────────────
def _get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


# ─── Cart views ───────────────────────────────────────────────────────────────
def cart_view(request):
    cart  = _get_cart(request)
    items = cart.items.select_related('product').prefetch_related('product__images')

    coupon = None
    discount = 0
    code = request.session.get('coupon_code', '')
    if code:
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.is_valid:
                discount = cart.total * coupon.discount_percent / 100
            else:
                del request.session['coupon_code']
                coupon = None
        except Coupon.DoesNotExist:
            request.session.pop('coupon_code', None)

    return render(request, 'orders/cart.html', {
        'cart': cart, 'items': items,
        'coupon': coupon, 'discount': discount,
        'grand_total': cart.total - discount,
    })


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    try:
        qty = max(1, int(request.POST.get('quantity', 1)))
    except (ValueError, TypeError):
        qty = 1

    if qty > product.stock:
        messages.error(request, f'Only {product.stock} items available.')
        return redirect('products:detail', slug=product.slug)

    cart = _get_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity = min(item.quantity + qty, product.stock)
    else:
        item.quantity = qty
    item.save()
    messages.success(request, f'"{product.name}" added to cart.')
    next_url = _safe_next(request)
    return redirect(next_url)


@require_POST
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    try:
        qty = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        qty = 1
    if qty < 1:
        item.delete()
    else:
        item.quantity = min(qty, item.product.stock)
        item.save()
    next_url = _safe_next(request)
    return redirect(next_url)


@require_POST
def remove_from_cart(request, item_id):
    get_object_or_404(CartItem, pk=item_id).delete()
    messages.success(request, 'Item removed.')
    next_url = _safe_next(request)
    return redirect(next_url)


@require_POST
def apply_coupon(request):
    code = request.POST.get('coupon_code', '').strip().upper()
    try:
        coupon = Coupon.objects.get(code=code)
        if not coupon.is_valid:
            messages.error(request, 'This coupon has expired or is no longer valid.')
        else:
            cart = _get_cart(request)
            if cart.total < coupon.min_order_amount:
                messages.error(request, f'Minimum order ৳{coupon.min_order_amount} required for this coupon.')
            else:
                request.session['coupon_code'] = code
                messages.success(request, f'Coupon "{code}" applied — {coupon.discount_percent}% off!')
    except Coupon.DoesNotExist:
        messages.error(request, 'Invalid coupon code.')
    return redirect('orders:cart')


@require_POST
def remove_coupon(request):
    request.session.pop('coupon_code', None)
    messages.info(request, 'Coupon removed.')
    return redirect('orders:cart')


# ─── Checkout ─────────────────────────────────────────────────────────────────
def checkout_view(request):
    cart = _get_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('orders:cart')

    coupon   = None
    discount = 0
    code     = request.session.get('coupon_code', '')
    if code:
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.is_valid:
                discount = cart.total * coupon.discount_percent / 100
        except Coupon.DoesNotExist:
            pass

    # Pre-fill from saved default address
    initial = {}
    if request.user.is_authenticated:
        addr = request.user.addresses.filter(is_default=True).first()
        if addr:
            initial = {
                'first_name': addr.full_name.split()[0] if addr.full_name else '',
                'last_name':  ' '.join(addr.full_name.split()[1:]) if addr.full_name else '',
                'email':      request.user.email,
                'phone':      addr.phone,
                'address':    addr.address_line,
                'city':       addr.city,
                'state':      addr.state,
                'zip_code':   addr.zip_code,
                'country':    addr.country,
            }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            order = Order.objects.create(
                user           = request.user if request.user.is_authenticated else None,
                first_name     = d['first_name'],
                last_name      = d.get('last_name', ''),
                email          = d['email'],
                phone          = d['phone'],
                address        = d['address'],
                city           = d['city'],
                state          = d.get('state', ''),
                zip_code       = d.get('zip_code', ''),
                country        = d['country'],
                payment_method = d['payment_method'],
                notes          = d.get('notes', ''),
                coupon_code    = code,
                discount_amount= round(discount, 2),
            )
            for item in cart.items.select_related('product'):
                OrderItem.objects.create(
                    order        = order,
                    product      = item.product,
                    product_name = item.product.name,
                    price        = item.product.effective_price,
                    quantity     = item.quantity,
                )
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save(update_fields=['stock'])

            if coupon:
                coupon.used_count += 1
                coupon.save(update_fields=['used_count'])
                request.session.pop('coupon_code', None)

            cart.items.all().delete()
            _send_order_email(order)
            return redirect('orders:success', order_number=order.order_number)
    else:
        form = CheckoutForm(initial=initial)

    items = cart.items.select_related('product').prefetch_related('product__images')
    return render(request, 'orders/checkout.html', {
        'form': form, 'cart': cart, 'items': items,
        'coupon': coupon, 'discount': discount,
        'grand_total': cart.total - discount,
    })


def order_success_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


# ─── Email helper ─────────────────────────────────────────────────────────────
def _send_order_email(order):
    try:
        items_text = '\n'.join(
            f'  - {i.product_name} ×{i.quantity}  ৳{i.subtotal}' for i in order.items.all()
        )
        body = (
            f"Hi {order.first_name},\n\n"
            f"Thank you for your order at {settings.SITE_NAME}!\n\n"
            f"Order Number : {order.order_number}\n"
            f"Payment      : {order.get_payment_method_display()}\n\n"
            f"Items:\n{items_text}\n\n"
            f"Total        : ৳{order.total}\n\n"
            f"Ship to      : {order.address}, {order.city}, {order.country}\n\n"
            f"We'll notify you when your order ships.\n\nThanks,\n{settings.SITE_NAME} Team"
        )
        send_mail(
            subject=f'Order Confirmed — {order.order_number}',
            message=body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            recipient_list=[order.email],
            fail_silently=True,
        )
    except Exception:
        pass
