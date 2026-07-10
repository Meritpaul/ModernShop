from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import BlogCategory, Post, Comment


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display       = ('name', 'post_count')
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display       = ('thumb', 'title', 'author', 'category', 'published_badge', 'views', 'created_at')
    list_display_links = ('thumb', 'title')
    list_filter        = ('is_published', 'category')
    search_fields      = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy     = 'created_at'
    fieldsets          = (
        (None,        {'fields': ('title', 'slug', 'author', 'category', 'thumbnail')}),
        ('Content',   {'fields': ('excerpt', 'body', 'tags')}),
        ('Settings',  {'fields': ('is_published',)}),
    )

    def thumb(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" class="admin-thumb">', obj.thumbnail.url)
        return mark_safe('<div style="width:48px;height:48px;border-radius:8px;background:#f1f5f9;"></div>')
    thumb.short_description = ''

    def published_badge(self, obj):
        if obj.is_published:
            return mark_safe('<span style="color:#10b981;font-weight:700;">● Published</span>')
        return mark_safe('<span style="color:#94a3b8;font-weight:700;">● Draft</span>')
    published_badge.short_description = 'Status'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('name', 'post', 'short_body', 'approved_badge', 'created_at')
    list_filter   = ('is_approved',)
    search_fields = ('name', 'email', 'body')
    actions       = ['approve', 'disapprove']

    def short_body(self, obj):
        return obj.body[:70] + ('…' if len(obj.body) > 70 else '')
    short_body.short_description = 'Comment'

    def approved_badge(self, obj):
        if obj.is_approved:
            return mark_safe('<span style="color:#10b981;font-weight:700;">✓ Approved</span>')
        return mark_safe('<span style="color:#ef4444;font-weight:700;">✗ Pending</span>')
    approved_badge.short_description = 'Status'

    def approve(self, request, qs):    qs.update(is_approved=True)
    def disapprove(self, request, qs): qs.update(is_approved=False)
    approve.short_description    = 'Approve selected comments'
    disapprove.short_description = 'Disapprove selected comments'
