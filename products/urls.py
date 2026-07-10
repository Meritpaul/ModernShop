from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',             views.shop_view,           name='shop'),
    path('<slug:slug>/', views.product_detail_view, name='detail'),
]
