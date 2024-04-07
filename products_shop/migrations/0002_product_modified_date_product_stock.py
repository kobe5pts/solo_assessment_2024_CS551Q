# Generated by Django 4.1.2 on 2024-04-06 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=1),
        ),
    ]