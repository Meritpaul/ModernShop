from .models import Cart


def cart_context(request):
    """Inject cart count, total and items into every template (for navbar badge + floating mini-cart)."""
    count = 0
    total = 0
    items = []
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            sk = request.session.session_key
            cart = Cart.objects.filter(session_key=sk).first() if sk else None
        if cart:
            count = cart.item_count
            total = cart.total
            items = list(cart.items.select_related('product').prefetch_related('product__images'))
    except Exception:
        pass
    return {'cart_count': count, 'cart_total': total, 'mini_cart_items': items}
