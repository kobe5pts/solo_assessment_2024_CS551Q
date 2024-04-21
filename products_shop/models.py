from django.db import models
from django.utils.text import slugify
from category.models import Category
import itertools
from django.urls import reverse

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField(blank=True)
    image_url = models.URLField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    stock = models.IntegerField(default=1)  # default set to 1, since each product has only one item on the CSV file 
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    # Define Meta class to specify ordering
    class Meta:
        ordering = ('-created',)

    # Define save method to generate unique slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = orig = slugify(self.product_name)[:255]  # Limit the length to 255 characters
            for x in itertools.count(1):
                if not Product.objects.filter(slug=self.slug).exists():
                    break
                # Truncate the original slug dynamically. Minus 1 for the hyphen we append.
                self.slug = "%s-%d" % (orig[:(len(orig)-len(str(x))-1)], x)
        super().save(*args, **kwargs)

    # Define method to get product URL
    def get_product_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    # Define string representation of the Product model
    def __str__(self):
        return self.product_name