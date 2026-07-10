from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/',                         views.cart_view,          name='cart'),
    path('cart/add/<int:product_id>/',    views.add_to_cart,        name='add_to_cart'),
    path('cart/update/<int:item_id>/',    views.update_cart,        name='update_cart'),
    path('cart/remove/<int:item_id>/',    views.remove_from_cart,   name='remove_from_cart'),
    path('cart/coupon/apply/',            views.apply_coupon,       name='apply_coupon'),
    path('cart/coupon/remove/',           views.remove_coupon,      name='remove_coupon'),
    path('checkout/',                     views.checkout_view,      name='checkout'),
    path('success/<str:order_number>/',   views.order_success_view, name='success'),
    path('history/',                      views.order_history_view, name='history'),
    path('detail/<str:order_number>/',    views.order_detail_view,  name='detail'),
]
