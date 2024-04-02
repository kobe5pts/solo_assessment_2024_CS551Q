from django.db import models
from category.models import Category

# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    description     = models.TextField(blank=True)
    price           = models.DecimalField(max_digits=4, decimal_places=2)
    category        = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    image           = models.ImageField(upload_to='images/')
    slug            = models.SlugField(max_length=200, unique=True)
    in_stock        = models.BooleanField(default=True)
    is_active       = models.BooleanField(default=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)


    def __str__(self):
        return self.product_name
