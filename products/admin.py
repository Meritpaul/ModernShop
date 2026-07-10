from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Review, Coupon


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('thumb', 'name', 'parent', 'product_count', 'is_active')
    list_display_links = ('thumb', 'name')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter   = ('is_active', 'parent')

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="admin-thumb">', obj.image.url)
        return mark_safe('<div style="width:42px;height:42px;border-radius:6px;background:#f1f5f9;"></div>')
    thumb.short_description = ''

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


class ProductImageInline(admin.TabularInline):
    model          = ProductImage
    extra          = 1
    fields         = ('preview', 'image', 'alt_text', 'is_primary', 'order')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="admin-thumb">', obj.image.url)
        return '—'
    preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('thumb', 'name', 'category', 'price_display', 'stock_display', 'badge', 'is_active', 'is_featured', 'avg_rating_display')
    list_display_links = ('thumb', 'name')
    list_filter   = ('is_active', 'is_featured', 'badge', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured', 'badge')
    inlines       = [ProductImageInline]
    list_per_page = 20
    fieldsets     = (
        ('Basic Information', {'fields': ('name', 'slug', 'category', 'description')}),
        ('Pricing & Inventory', {'fields': (('price', 'sale_price'), 'stock')}),
        ('Display', {'fields': ('badge', 'is_active', 'is_featured')}),
    )

    def thumb(self, obj):
        img = obj.main_image
        if img:
            return format_html('<img src="{}" class="admin-thumb">', img.image.url)
        return mark_safe('<div style="width:48px;height:48px;border-radius:8px;background:#f1f5f9;display:flex;align-items:center;justify-content:center;color:#94a3b8;font-size:11px;">No img</div>')
    thumb.short_description = ''

    def price_display(self, obj):
        if obj.sale_price:
            return format_html('<s style="color:#94a3b8;font-size:12px;">৳{}</s> <strong style="color:#dc3545;">৳{}</strong>', obj.price, obj.sale_price)
        return format_html('<strong>৳{}</strong>', obj.price)
    price_display.short_description = 'Price'

    def stock_display(self, obj):
        color = '#dc3545' if obj.stock == 0 else ('#f59e0b' if obj.stock < 10 else '#10b981')
        return format_html('<span style="color:{};font-weight:700;">{}</span>', color, obj.stock)
    stock_display.short_description = 'Stock'

    def avg_rating_display(self, obj):
        r = obj.avg_rating
        if r:
            stars = '★' * int(r) + '☆' * (5 - int(r))
            return format_html('<span style="color:#f59e0b;">{}</span> <small style="color:#94a3b8;">({})</small>', stars, obj.review_count)
        return mark_safe('<small style="color:#94a3b8;">No reviews</small>')
    avg_rating_display.short_description = 'Rating'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('product', 'user', 'stars_display', 'title', 'is_approved', 'created_at')
    list_filter   = ('is_approved', 'rating')
    list_editable = ('is_approved',)
    search_fields = ('product__name', 'user__email', 'title')
    date_hierarchy = 'created_at'

    def stars_display(self, obj):
        return format_html('<span style="color:#f59e0b;">{}</span>', '★' * obj.rating + '☆' * (5 - obj.rating))
    stars_display.short_description = 'Rating'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display  = ('code', 'discount_percent', 'usage_bar', 'min_order_amount', 'status_display', 'valid_to')
    list_filter   = ('is_active',)
    search_fields = ('code',)

    def usage_bar(self, obj):
        pct = min(int(obj.used_count / obj.max_uses * 100), 100) if obj.max_uses else 0
        return format_html(
            '<div style="width:100px;background:#e5e7eb;border-radius:4px;overflow:hidden;">'
            '<div style="width:{}%;background:#1a1a2e;height:8px;"></div></div>'
            '<small style="color:#6b7280;">{} / {}</small>',
            pct, obj.used_count, obj.max_uses)
    usage_bar.short_description = 'Usage'

    def status_display(self, obj):
        if obj.is_valid:
            return mark_safe('<span style="color:#10b981;font-weight:700;">● Active</span>')
        return mark_safe('<span style="color:#dc3545;font-weight:700;">● Inactive</span>')
    status_display.short_description = 'Status'
