"""
cPanel 'Setup Python App' entry point.
  Application startup file : passenger_wsgi.py
  Application Entry point  : application
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modernshop.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
