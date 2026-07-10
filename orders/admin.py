from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Cart, CartItem, Order, OrderItem

STATUS_COLORS = {
    'pending':    '#6b7280',
    'confirmed':  '#3b82f6',
    'processing': '#f59e0b',
    'shipped':    '#06b6d4',
    'delivered':  '#10b981',
    'cancelled':  '#ef4444',
}


class OrderItemInline(admin.TabularInline):
    model           = OrderItem
    extra           = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'subtotal')
    can_delete      = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('order_number', 'full_name', 'status_badge', 'payment_method', 'paid_badge', 'total_display', 'created_at')
    list_filter     = ('status', 'payment_method', 'is_paid')
    search_fields   = ('order_number', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('order_number', 'subtotal', 'total', 'created_at', 'updated_at')
    inlines         = [OrderItemInline]
    date_hierarchy  = 'created_at'
    list_per_page   = 25
    fieldsets       = (
        ('Order Info',    {'fields': ('order_number', ('status', 'is_paid'), 'payment_method', ('coupon_code', 'discount_amount'))}),
        ('Customer',      {'fields': (('first_name', 'last_name'), 'email', 'phone')}),
        ('Shipping',      {'fields': ('address', ('city', 'state'), ('zip_code', 'country'), 'notes')}),
        ('Totals',        {'fields': ('subtotal', 'total')}),
        ('Timestamps',    {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    actions = ['mark_confirmed', 'mark_shipped', 'mark_delivered', 'mark_cancelled']

    def status_badge(self, obj):
        color = STATUS_COLORS.get(obj.status, '#6b7280')
        return format_html('<span class="status-pill" style="background:{};">{}</span>', color, obj.get_status_display().upper())
    status_badge.short_description = 'Status'

    def paid_badge(self, obj):
        if obj.is_paid:
            return mark_safe('<span style="color:#10b981;font-weight:700;">✓ Paid</span>')
        return mark_safe('<span style="color:#ef4444;font-weight:700;">✗ Unpaid</span>')
    paid_badge.short_description = 'Payment'

    def total_display(self, obj):
        return format_html('<strong>৳{}</strong>', f'{obj.total:.2f}')
    total_display.short_description = 'Total'

    def mark_confirmed(self, request, qs):  qs.update(status='confirmed')
    def mark_shipped(self, request, qs):    qs.update(status='shipped')
    def mark_delivered(self, request, qs):  qs.update(status='delivered')
    def mark_cancelled(self, request, qs):  qs.update(status='cancelled')

    mark_confirmed.short_description = 'Mark as Confirmed'
    mark_shipped.short_description   = 'Mark as Shipped'
    mark_delivered.short_description = 'Mark as Delivered'
    mark_cancelled.short_description = 'Mark as Cancelled'


class CartItemInline(admin.TabularInline):
    model  = CartItem
    extra  = 0
    fields = ('product', 'quantity')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item_count_display', 'total_display', 'updated_at')
    inlines      = [CartItemInline]

    def item_count_display(self, obj): return obj.item_count
    def total_display(self, obj):      return f'৳{obj.total}'
    item_count_display.short_description = 'Items'
    total_display.short_description      = 'Total'
