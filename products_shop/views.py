from django.shortcuts import render, get_object_or_404
from . models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


# Create your views here.

def store(request, category_slug= None):
    categories = None
    products   = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products   = Product.objects.filter(category=categories, in_stock=True)
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:    
        products = Product.objects.all().filter(in_stock=True).order_by('id')
        paginator = Paginator(products, 50)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    context = {
        'products': paged_products,
        'product_count': product_count,
    }    
    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        In_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
      raise e 
    context = {
        'single_product' : single_product,
        'In_cart' : In_cart,
    }  
    return render(request, 'store/product_detail.html', context)


def search(request):
    # Get the keyword from the request
    keyword = request.GET.get('keyword', '').strip()

    products = None
    product_count = 0
    paged_products = None

    if keyword:  
        # Check if keyword is not empty
        products = Product.objects.order_by('-created').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))

        paginator = Paginator(products, 50)  # Define the number of items per page
        page_number = request.GET.get('page')
        paged_products = paginator.get_page(page_number)

        product_count = products.count()

        # Loop over the paginator's page range to ensure both keyword and page number are available
        for page_num in paged_products.paginator.page_range:
            paged_products.object_list[page_num - 1].keyword = keyword

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)