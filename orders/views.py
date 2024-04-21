from django.shortcuts import render, redirect
from carts.models import CartItem
import datetime
from .forms import OrderForm
from .models import Order, OrderProduct
from datetime import datetime
import logging
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

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
            current_date = datetime.now().strftime("%d%m%Y")  # Format: DDMMYYYY
            order_number = f"{current_date}{data.id}"
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


logger = logging.getLogger(__name__)

def order_complete(request):
    order_number = request.GET.get('order_number')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=False)

        # Update order status to 'Completed'
        order.status = 'Completed'
        order.save()

        ordered_products = OrderProduct.objects.filter(order=order, ordered=False)

        subtotal = 0
        for item in ordered_products:
            subtotal += item.product_price * item.quantity

        # Delete cart items associated with the current user
        if request.user.is_authenticated:
            CartItem.objects.filter(user=request.user).delete()

        # Update context with order status
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'subtotal': subtotal,
            'status': 'Completed',  # Add order status to the context
        }

        return render(request, 'orders/order_complete.html', context)
    except Order.DoesNotExist:
        return redirect('home')