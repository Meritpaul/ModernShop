from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category, Review
from .forms import ReviewForm


def shop_view(request):
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')

    # Search
    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # Category filter
    cat_slug = request.GET.get('category', '').strip()
    active_category = None
    if cat_slug:
        active_category = get_object_or_404(Category, slug=cat_slug, is_active=True)
        products = products.filter(Q(category=active_category) | Q(category__parent=active_category))

    # Price filter
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Badge filter
    badge = request.GET.get('badge', '').strip()
    if badge:
        products = products.filter(badge=badge)

    # Sort
    sort_map = {
        'newest':     '-created_at',
        'price_asc':  'price',
        'price_desc': '-price',
        'name':       'name',
    }
    sort = request.GET.get('sort', 'newest')
    products = products.order_by(sort_map.get(sort, '-created_at'))

    total = products.count()
    paginator = Paginator(products, 9)
    page_obj  = paginator.get_page(request.GET.get('page'))

    categories = Category.objects.filter(is_active=True, parent=None).prefetch_related('children')

    return render(request, 'products/shop.html', {
        'page_obj': page_obj, 'categories': categories,
        'active_category': active_category, 'q': q,
        'sort': sort, 'min_price': min_price, 'max_price': max_price,
        'total': total, 'badge': badge,
    })


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images  = product.images.all()
    reviews = product.reviews.filter(is_approved=True).select_related('user')
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]

    user_reviewed = False
    form = ReviewForm()

    if request.user.is_authenticated:
        user_reviewed = reviews.filter(user=request.user).exists()
        if request.method == 'POST':
            if user_reviewed:
                messages.warning(request, 'You have already reviewed this product.')
            else:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    r = form.save(commit=False)
                    r.product = product
                    r.user    = request.user
                    r.save()
                    messages.success(request, 'Review submitted!')
                    return redirect('products:detail', slug=slug)

    return render(request, 'products/product_detail.html', {
        'product': product, 'images': images, 'reviews': reviews,
        'related': related, 'form': form, 'user_reviewed': user_reviewed,
    })
