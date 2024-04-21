from django import forms
from .models import UserProfile

# Define a registration form for user profiles
class RegistrationForm(forms.ModelForm):
    """
    Form for user registration with custom fields and validations.
    """
    # Password field with password input widget
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
        'class' : 'form-control',
    }))

    # Repeat password field with password input widget
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Repeat Password'
    }))
    class Meta:
        model = UserProfile
        # Define fields to be included in the form
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'username', 'address', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Set placeholder and class attributes for form fields
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter User Name'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        # Retrieve password and repeat password from cleaned data
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        # Check if passwords match, raise validation error if not
        if password != repeat_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

