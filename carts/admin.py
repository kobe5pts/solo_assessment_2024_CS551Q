from django.contrib import admin
from . models import Cart, CartItem

# Register your models here.

# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('product_name',)}
#     list_display = ('product_name', 'price', 'stock', 'in_stock','is_active', 'category', 'modified_date')

admin.site.register(Cart)
admin.site.register(CartItem)