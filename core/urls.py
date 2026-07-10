from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',         views.home_view,    name='home'),
    path('about/',   views.about_view,   name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('faq/',     views.faq_view,     name='faq'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_view, name='terms'),
    path('refund-policy/', views.refund_policy_view, name='refund_policy'),
]
