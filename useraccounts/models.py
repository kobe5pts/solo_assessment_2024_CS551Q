from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# # Create your models here.

# Custom user manager for the UserProfile model
class AccountManager(BaseUserManager):
    """
    Custom user manager for managing user creation and superuser creation.
    """
    def create_user(self, first_name, last_name, username, email, phone_number, address, password=None):
        """
        Method to create a regular user.
        """
        # Check if email is provided
        if not email:
            raise Valueerror('you must have an email')

        # Check if username is provided
        if not username:
            raise Valueerror('you must provide a username')

        # Create a new user object
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            address = address,
        )

        # Set password and save the user
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def  create_superuser(self, first_name, last_name, username, email, password):
        """
        Method to create a superuser.
        """
        # Create a regular user first
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,  
        )
        # Set superuser attributes and save
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

# Custom user profile model extending AbstractBaseUser
class UserProfile(AbstractBaseUser):
    """
    Custom user profile model extending AbstractBaseUser.
    """
    # Define user profile fields
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=50, unique=True)
    address         = models.CharField(max_length=200)
    phone_number    = models.CharField(max_length=20)

    # Required fields for user model
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS  = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin    

    def has_module_perms(self, add_label):
        return True

