from django.contrib import admin
from .models import Cart, Category, MenuItem, Order

# Register your models here.
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
