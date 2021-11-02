from django.urls import path
from . import views

app_name = 'ecom'

urlpatterns = [
    path('',views.all_products, name="all_products"),
    path('product_detail/<int:pk>/', views.productDetail , name="product_detail"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('updateItem/',views.updateItem, name="updateItem"),
    path('all_order_items/',views.all_order_items, name="all_order_items"),
    path('order_success/<int:order_id>/',views.order_success, name="order_success"),
    path('buynow/<int:pk>/',views.buynow, name="buynow"),
]