from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView, RedirectView
from core.sitemaps import StaticViewSitemap, ProductSitemap, BlogPostSitemap

sitemaps = {
    'static':  StaticViewSitemap,
    'products': ProductSitemap,
    'blog':    BlogPostSitemap,
}

urlpatterns = [
    # must stay ABOVE 'admin/' include, otherwise admin.site.urls swallows this path
    path('admin/password_reset/',
         RedirectView.as_view(pattern_name='users:password_reset', permanent=False),
         name='admin_password_reset'),

    path('admin/', admin.site.urls),
    path('',        include('core.urls')),
    path('users/',  include('users.urls')),
    path('shop/',   include('products.urls')),
    path('orders/', include('orders.urls')),
    path('blog/',   include('blog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
