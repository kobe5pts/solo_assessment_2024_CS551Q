from django import forms
from .models import Order

# Define the OrderForm class
class OrderForm(forms.ModelForm):
    # Meta class specifying the model and fields
    class Meta:
        model = Order
        # Specify the fields to include in the form
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']