from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from carts.views import _cart_id
from django.contrib.auth import authenticate
from orders.models import Order
from django.db.models import Count
from django.db.models.functions import TruncMonth

# Create your views here.

# Views for user account functionality

def register(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # If form is valid, create a new user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            user = UserProfile.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, username=username, address=address, password=password)
            user.save()
            messages.success(request, 'Registration is Successful!')
            return redirect('register')
    else:
        form = RegistrationForm()       
    context = {
       'form' : form,
    }
    return render(request, 'useraccounts/register.html', context)


def login(request):
    """
    View for user login.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            try:
                # Transfer cart items to user after login
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    for item in cart_items:
                        item.user = user
                        item.save()
            except:
                pass
            
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                # Redirect to previous page after login
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'useraccounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    """
    View for user logout.
    """
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    """
    View for user dashboard.
    """
    # Check if the user is an admin
    if request.user.is_admin:
        # If the user is an admin, proceed with the existing logic
        orders = Order.objects.filter(user_id=request.user.id, is_ordered=True)
        orders_by_month = orders.annotate(order_month=TruncMonth('created_at')).values('order_month').annotate(count=Count('id')).order_by('order_month')
        months = [order['order_month'].strftime('%b %Y') for order in orders_by_month]
        counts = [order['count'] for order in orders_by_month]
        context = {
            'orders_count': orders.count(),
            'order_months': months,
            'order_counts': counts,
        }
    else:
        # If the user is not an admin, return the view for ordered orders
        orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=False)
        orders_count = orders.count()
        context = {
            'orders_count': orders_count,
        }
        
    return render(request, 'useraccounts/dashboard.html', context)