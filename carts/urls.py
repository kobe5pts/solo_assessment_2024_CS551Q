# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.cart, name='cart'),
#     path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
#     path('decrement_cart/<int:product_id>/', views.decrement_cart, name='decrement_cart'),
#     path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
#     path('checkout/', views.checkout, name='checkout'),
# ]

from django.urls import path
from . import views

# Define URL patterns for the cart app
urlpatterns = [
    # URL pattern for the cart page
    path('', views.cart, name='cart'),
    
    # URL pattern for adding a product to the cart
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    
    # URL pattern for decrementing the quantity of a product in the cart
    path('decrement_cart/<int:product_id>/', views.decrement_cart, name='decrement_cart'),
    
    # URL pattern for removing a specific item from the cart
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    
    # URL pattern for the checkout page
    path('checkout/', views.checkout, name='checkout'),
]
