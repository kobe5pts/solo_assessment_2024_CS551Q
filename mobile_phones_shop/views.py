from django.shortcuts import render
from products_shop.models import Product

def homepage(request):
    products = Product.objects.all().filter(in_stock=True)
    
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)
