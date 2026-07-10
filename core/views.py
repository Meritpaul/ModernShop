from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from products.models import Product, Category
from blog.models import Post


def home_view(request):
    featured   = Product.objects.filter(is_active=True, is_featured=True).prefetch_related('images')[:8]
    new_items  = Product.objects.filter(is_active=True, badge='new').prefetch_related('images')[:8]
    sale_items = Product.objects.filter(is_active=True, badge='sale').prefetch_related('images')[:4]
    categories = Category.objects.filter(is_active=True, parent=None)[:6]
    posts      = Post.objects.filter(is_published=True).select_related('author', 'category')[:3]
    return render(request, 'core/home.html', {
        'featured': featured, 'new_items': new_items,
        'sale_items': sale_items, 'categories': categories, 'posts': posts,
    })


def about_view(request):
    team_members = [
        ('images/team/man1.jpg', 'Sarah Johnson', 'CEO & Founder'),
        ('images/team/woman1.jpg', 'Michael Chen', 'Head of Design'),
        ('images/team/woman2.jpg', 'Emily Davis', 'Marketing Lead'),
        ('images/team/man1.jpg', 'James Wilson', 'Tech Lead'),
    ]
    return render(request, 'core/about.html', {'team_members': team_members})


def contact_view(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        msg     = request.POST.get('message', '').strip()
        if name and email and msg:
            try:
                send_mail(
                    subject=f'[Contact Form] {subject or "New message from " + name}',
                    message=f'Name: {name}\nEmail: {email}\n\n{msg}',
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
        else:
            messages.error(request, 'Please fill in all required fields.')
        return redirect('core:contact')
    return render(request, 'core/contact.html')


def faq_view(request):
    return render(request, 'core/faq.html')


def privacy_policy_view(request):
    return render(request, 'core/privacy_policy.html')


def terms_view(request):
    return render(request, 'core/terms.html')


def refund_policy_view(request):
    return render(request, 'core/refund_policy.html')


def handler404(request, exception=None):
    return render(request, 'core/404.html', status=404)


def handler500(request):
    return render(request, 'core/500.html', status=500)
