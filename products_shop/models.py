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
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = orig = slugify(self.product_name)[:255]  # Limit the length to 255 characters
            for x in itertools.count(1):
                if not Product.objects.filter(slug=self.slug).exists():
                    break
                # Truncate the original slug dynamically. Minus 1 for the hyphen we append.
                self.slug = "%s-%d" % (orig[:(len(orig)-len(str(x))-1)], x)
        super().save(*args, **kwargs)

    def get_product_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name