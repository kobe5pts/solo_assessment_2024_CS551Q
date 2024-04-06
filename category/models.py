from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.cat_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cat_name
