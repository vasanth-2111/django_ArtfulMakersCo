# Generated by Django 4.2.7 on 2023-12-21 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crafts', '0003_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=60),
        ),
    ]
