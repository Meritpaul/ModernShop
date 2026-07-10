import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Site branding ──────────────────────────────────────────────────────────
# পুরো ওয়েবসাইটের নাম এখানে এক জায়গায় সেট করা। ভবিষ্যতে নাম বদলাতে চাইলে
# শুধু এই একটা লাইন বদলালেই (অথবা .env এ SITE_NAME=NewName দিলেই) সব
# জায়গায় (navbar, footer, page title, email) নতুন নাম দেখাবে।
SITE_NAME = config('SITE_NAME', default='ModernShop')

# ─── Security ────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-local-dev-only-change-in-production')
DEBUG      = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

_csrf = config('CSRF_TRUSTED_ORIGINS', default='')
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf.split(',') if o.strip()]

# ─── Apps ─────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'jazzmin',                              # Must be BEFORE django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'users',
    'products',
    'orders',
    'blog',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'modernshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'orders.context_processors.cart_context',
                'products.context_processors.categories_context',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'modernshop.wsgi.application'

# ─── Database ─────────────────────────────────────────────────────────────────
# Local dev: SQLite (no config needed)
# Live (cPanel): set DB_ENGINE=mysql + DB_NAME + DB_USER + DB_PASSWORD in .env
if config('DB_ENGINE', default='sqlite') == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME':     config('DB_NAME'),
            'USER':     config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST':     config('DB_HOST', default='localhost'),
            'PORT':     config('DB_PORT', default='3306'),
            'OPTIONS':  {'charset': 'utf8mb4'},
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─── Password validation ──────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Localisation ────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Dhaka'
USE_I18N = True
USE_TZ   = True

# ─── Static & Media ───────────────────────────────────────────────────────────
STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT      = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── Auth ────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD  = 'django.db.models.BigAutoField'
AUTH_USER_MODEL     = 'users.User'
LOGIN_URL           = '/users/login/'
LOGIN_REDIRECT_URL  = '/'
LOGOUT_REDIRECT_URL = '/'

# ─── Email ────────────────────────────────────────────────────────────────────
# Local: prints to console. Live: fill EMAIL_HOST_USER + EMAIL_HOST_PASSWORD in .env
if config('EMAIL_HOST_USER', default=''):
    EMAIL_BACKEND      = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST         = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT         = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS      = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER    = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD= config('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ─── Contact form recipient ────────────────────────────────────────────────────
# যেই ইমেইলে কাস্টমারদের Contact Us ফর্মের মেসেজ যাবে।
# .env এ CONTACT_EMAIL=youremail@gmail.com দিয়ে বদলাতে পারবে।
CONTACT_EMAIL = config('CONTACT_EMAIL', default='support@modernshop.com')

# ─── Production security (only when DEBUG=False) ──────────────────────────────
if not DEBUG:
    SECURE_SSL_REDIRECT            = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE          = True
    CSRF_COOKIE_SECURE             = True
    SECURE_BROWSER_XSS_FILTER      = True
    SECURE_CONTENT_TYPE_NOSNIFF    = True
    X_FRAME_OPTIONS                = 'DENY'
    SECURE_HSTS_SECONDS            = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD            = True
    SECURE_PROXY_SSL_HEADER        = ('HTTP_X_FORWARDED_PROTO', 'https')

# ─── Logging ──────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file':    {'class': 'logging.FileHandler', 'filename': BASE_DIR / 'error.log', 'level': 'ERROR'},
    },
    'root': {
        'handlers': ['console'] if DEBUG else ['file'],
        'level': 'WARNING',
    },
}

# ─── Jazzmin Admin Theme ──────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    'site_title':    f'{SITE_NAME} Admin',
    'site_header':   SITE_NAME,
    'site_brand':    SITE_NAME,
    'welcome_sign':  f'Welcome to {SITE_NAME} Admin',
    'copyright':     SITE_NAME,
    'search_model':  ['products.Product', 'orders.Order', 'users.User'],

    # Top bar links — including "View Website" so admin can check live site
    'topmenu_links': [
        {'name': 'View Website',  'url': '/',       'new_window': True, 'icon': 'fas fa-external-link-alt'},
        {'name': 'Shop',          'url': '/shop/',  'new_window': True, 'icon': 'fas fa-store'},
    ],

    'show_sidebar':           True,
    'navigation_expanded':    True,
    'order_with_respect_to':  ['products', 'orders', 'users', 'blog', 'core', 'auth'],
    'related_modal_active':   True,
    'custom_css':             'css/admin_custom.css',
    'use_google_fonts_cdn':   True,
    'show_ui_builder':        False,
    'changeform_format':      'horizontal_tabs',

    'icons': {
        'auth':              'fas fa-users-cog',
        'users.User':        'fas fa-user-circle',
        'users.Address':     'fas fa-map-marker-alt',
        'products.Category': 'fas fa-tags',
        'products.Product':  'fas fa-box-open',
        'products.ProductImage': 'fas fa-images',
        'products.Review':   'fas fa-star',
        'products.Coupon':   'fas fa-ticket-alt',
        'orders.Order':      'fas fa-shopping-cart',
        'orders.Cart':       'fas fa-shopping-basket',
        'blog.Post':         'fas fa-newspaper',
        'blog.BlogCategory': 'fas fa-folder-open',
        'blog.Comment':      'fas fa-comments',
    },
    'default_icon_parents':  'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text':          False,
    'footer_small_text':          False,
    'body_small_text':            False,
    'brand_small_text':           False,
    'brand_colour':               'navbar-dark',
    'accent':                     'accent-primary',
    'navbar':                     'navbar-dark',
    'navbar_fixed':               True,
    'layout_boxed':               False,
    'footer_fixed':               False,
    'sidebar_fixed':              True,
    'sidebar':                    'sidebar-dark-primary',
    'sidebar_nav_small_text':     False,
    'sidebar_nav_child_indent':   True,
    'sidebar_nav_compact_style':  False,
    'sidebar_nav_legacy_style':   False,
    'sidebar_nav_flat_style':     False,
    'theme':                      'default',
    'button_classes': {
        'primary':   'btn-dark',
        'secondary': 'btn-outline-secondary',
        'info':      'btn-info',
        'warning':   'btn-warning',
        'danger':    'btn-danger',
        'success':   'btn-success',
    },
    'actions_sticky_top': True,
}
