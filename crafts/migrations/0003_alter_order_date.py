# Generated by Django 4.2.7 on 2023-12-21 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crafts', '0002_order_remove_cartitem_cart_remove_cartitem_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]