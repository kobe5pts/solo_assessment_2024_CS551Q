from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# Register your models here.

class AccountAdmin(UserAdmin):
    """
    Custom admin configuration for UserProfile model.
    """
    # Display fields in the admin list view
    list_display = ('first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    # Readonly fields in the admin detail view
    readonly_fields = ('last_login', 'date_joined')
    # Ordering of records in the admin list view
    ordering = ('-date_joined',)

    # Define filter and fieldset configurations
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
# Register the UserProfile model with the custom admin configuration
admin.site.register(UserProfile, AccountAdmin)