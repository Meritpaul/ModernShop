from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import User, Address


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('avatar_thumb', 'email', 'username', 'full_name_display', 'role_badge', 'order_count', 'date_joined')
    list_display_links = ('avatar_thumb', 'email')
    list_filter   = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering      = ('-date_joined',)
    fieldsets     = BaseUserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone', 'avatar', 'bio')}),
    )

    def avatar_thumb(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" class="admin-thumb" style="border-radius:50%;">', obj.avatar.url)
        initial = (obj.username or obj.email or '?')[0].upper()
        return format_html(
            '<div style="width:36px;height:36px;border-radius:50%;background:#1a1a2e;color:#fff;'
            'display:flex;align-items:center;justify-content:center;font-weight:700;">{}</div>', initial)
    avatar_thumb.short_description = ''

    def full_name_display(self, obj):
        return obj.get_full_name() or '—'
    full_name_display.short_description = 'Name'

    def role_badge(self, obj):
        if obj.is_superuser:
            return mark_safe('<span class="status-pill" style="background:#1a1a2e;">Superuser</span>')
        if obj.is_staff:
            return mark_safe('<span class="status-pill" style="background:#0d6efd;">Staff</span>')
        return mark_safe('<span class="status-pill" style="background:#6c757d;">Customer</span>')
    role_badge.short_description = 'Role'

    def order_count(self, obj):
        return obj.orders.count()
    order_count.short_description = 'Orders'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'user', 'city', 'country', 'default_badge')
    list_filter   = ('country', 'is_default')
    search_fields = ('full_name', 'user__email', 'city')

    def default_badge(self, obj):
        return mark_safe('<span style="color:#28a745;font-weight:700;">★ Default</span>') if obj.is_default else ''
    default_badge.short_description = ''
