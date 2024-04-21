from django.shortcuts import render, get_object_or_404
from . models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.

def store(request, category_slug=None):
    """
    View function to display products in the store.

    Parameters:
    - request: HTTP request object
    - category_slug: Slug for category filtering (default: None)

    Returns:
    - Rendered HTML template displaying products in the store
    """
    categories = None
    products = None

    if category_slug:
        # Filter products by category if category_slug is provided
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, in_stock=True).order_by('id')
    else:
        # Otherwise, fetch all products
        products = Product.objects.filter(in_stock=True).order_by('id')

    # Paginate products
    paginator = Paginator(products, 50)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    product_count = products.count()

    # Context data to pass to the template
    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    """
    View function to display detailed information about a single product.

    Parameters:
    - request: HTTP request object
    - category_slug: Slug for category filtering
    - product_slug: Slug for product filtering

    Returns:
    - Rendered HTML template displaying product detail
    """
    # Fetch the single product based on category and product slugs
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    # Check if the product is already in the cart
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    """
    View function to perform product search.

    Parameters:
    - request: HTTP request object

    Returns:
    - Rendered HTML template displaying search results
    """
    keyword = request.GET.get('keyword', '').strip()
    products = None
    product_count = 0
    paged_products = None

    if keyword:
        # Perform search based on keyword matching product name or description
        products = Product.objects.filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('-created')

        # Paginate search results
        paginator = Paginator(products, 50)
        page_number = request.GET.get('page')
        product_count = products.count()

        try:
            paged_products = paginator.page(page_number)
            product_count = paginator.count

            for product in paged_products:
                product.keyword = keyword

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paged_products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paged_products = paginator.page(paginator.num_pages)

    # Context data to pass to the template
    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)
