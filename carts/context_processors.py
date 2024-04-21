from .models import Cart, CartItem
from .views import _cart_id

def cart_counter(request):
    """
    Counts the number of items in the user's cart and returns it as a context variable.
    
    Args:
    - request: HttpRequest object
    
    Returns:
    - Dictionary: A dictionary containing the cart count as a context variable.
    """
    cart_count = 0
    # Check if the request is for the admin page
    if 'admin' in request.path:
        return()
    else:
        try:
            # Retrieve the cart based on the session ID
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            # Check if the user is authenticated
            if request.user.is_authenticated: 
                # If authenticated, retrieve cart items associated with the user  
                cart_items = CartItem.objects.all().filter(user=request.user)
            else: 
                # If not authenticated, retrieve cart items associated with the cart   
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            # Calculate the total number of items in the cart
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            # If the cart does not exist, set the cart count to 0
            cart_item = 0
    # Return the cart count as a context variable
    return {'cart_count': cart_count}                

