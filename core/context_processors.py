from django.conf import settings


def site_settings(request):
    """Makes {{ site_name }} and {{ contact_email }} available in every template."""
    return {
        'site_name': settings.SITE_NAME,
        'contact_email': settings.CONTACT_EMAIL,
    }
