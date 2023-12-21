from django.contrib import admin
from .models import Artisan, Customer, Product, Order
# Register your models with the admin site
admin.site.register(Product)
admin.site.register(Artisan)
admin.site.register(Customer)

admin.site.register(Order)

