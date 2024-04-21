from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),     # URL pattern for the main store page
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),   # URL pattern to display products by category
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),    # URL pattern to display product detail
    path('search/', views.search, name='search'),   # URL pattern for search functionality
    ]