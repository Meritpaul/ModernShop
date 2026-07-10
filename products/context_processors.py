from .models import Category


def categories_context(request):
    """Inject top-level categories into every template (navbar mega-menu & footer)."""
    try:
        cats = Category.objects.filter(is_active=True, parent=None).prefetch_related('children')
    except Exception:
        cats = []
    return {'nav_categories': cats}
