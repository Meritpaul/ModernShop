from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product
from blog.models import Post


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return ['core:home', 'core:about', 'core:contact', 'core:faq',
                'products:shop', 'blog:list']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Product.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('products:detail', args=[obj.slug])


class BlogPostSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return Post.objects.filter(is_published=True)

    def location(self, obj):
        return reverse('blog:detail', args=[obj.slug])

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', None) or getattr(obj, 'created_at', None)
