from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(UserProfile, AccountAdmin)