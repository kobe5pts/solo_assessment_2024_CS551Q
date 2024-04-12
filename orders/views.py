from django.shortcuts import render, redirect
from carts.models import CartItem
import datetime
from .forms import OrderForm
from .models import Order, OrderProduct

# Create your views here.

# def place_order(request, total=0, quantity=0,):
#     current_user = request.user

#     # If the cart count is less than or equal to 0, then redirect back to products_shop
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect('store')

#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = round((5 * total) / 100, 2)
#     grand_total = total + tax

    
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # Store all the billing information inside Order table
#             data = Order()
#             data.user = current_user
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.tax = tax
#             data.save()
#             # Generate order number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr,mt,dt)
#             current_date = d.strftime("%d%m%Y") #10042024
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()

#                     # Move the cart items to Order Product table
#             # cart_items = CartItem.objects.filter(user=request.user)

#             for item in cart_items:
#                 orderproduct = OrderProduct()
#                 orderproduct.order_id = order.id
#                 # orderproduct.payment = payment
#                 orderproduct.user_id = request.user.id
#                 orderproduct.product_id = item.product_id
#                 orderproduct.quantity = item.quantity
#                 orderproduct.product_price = item.product.price
#                 orderproduct.ordered = False
#                 orderproduct.save()

#                 # cart_item = CartItem.objects.get(id=item.id)
#                 # product_variation = cart_item.variations.all()
#                 # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
#                 # orderproduct.variations.set(product_variation)
#                 # orderproduct.save()

#             # Redirect to order_complete view with order_number and additional data as query parameters
#             url = reverse('order_complete')
#             url += f'?order_number={order_number}'
#             url += f'&total={total}'
#             url += f'&tax={tax}'
#             url += f'&grand_total={grand_total}'
#             return HttpResponseRedirect(url)


#             order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
#             context = {
#                 'order': order,
#                 'cart_items': cart_items,
#                 'total': total,
#                 'tax': tax,
#                 'grand_total': grand_total,
#             }
#             # return render(request, 'orders/payments.html', context)
#             # Redirect to order_complete view with order_number as query parameter
#             return HttpResponseRedirect(f'/orders/order_complete/?order_number={order_number}')
#     else:
#         return redirect('checkout')

def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to products_shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = round((5 * total) / 100, 2)
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%d%m%Y") #10042024
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # Move the cart items to Order Product table
            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order = data  # Assign the order object to orderproduct.order
                orderproduct.user = current_user
                orderproduct.product = item.product
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = False
                orderproduct.save()

            # Redirect to order_complete view with order_number and additional data as query parameters
            return HttpResponseRedirect(f'/orders/order_complete/?order_number={order_number}&total={total}&tax={tax}&grand_total={grand_total}')

    else:
        return redirect('checkout')


import logging
from django.http import HttpResponseRedirect
from django.urls import reverse

logger = logging.getLogger(__name__)

def order_complete(request):
    order_number = request.GET.get('order_number')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=False)
        print("Order:", order)  # Print order object for debugging

        # ordered_products = OrderProduct.objects.filter(order_id=order.id, ordered=False)
        ordered_products = OrderProduct.objects.filter(order=order, ordered=False)
        print("Ordered Products:", ordered_products)  # Print ordered products for debugging

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

            # Delete cart items associated with the current user
        if request.user.is_authenticated:
            CartItem.objects.filter(user=request.user).delete()

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'subtotal': subtotal,
        }

        # Check if all required context keys are present
        # required_keys = ['order', 'ordered_products', 'order_number', 'subtotal']
        # if not all(key in context for key in required_keys):
        #     raise Http404("Some required context data is missing.")
        
        return render(request, 'orders/order_complete.html', context)
    except (Order.DoesNotExist):
        # logger.error(f"Order with order_number={order_number} does not exist.")
        return redirect('home')

# def payment(request):
#         # Clear cart
#     CartItem.objects.filter(user=request.user).delete()

#     return render('orders/payments.html')        
