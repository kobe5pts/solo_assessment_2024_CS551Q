# Generated by Django 4.1.2 on 2024-04-06 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products_shop', '0002_product_modified_date_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=200)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products_shop.product')),
            ],
        ),
    ]