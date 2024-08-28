from django.db import models
from django.contrib.auth.models import User, Group

class Category(models.Model):
    name = models.CharField(max_length=100)

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_item_of_the_day = models.BooleanField(default=False)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem)
    order_date = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    delivery_crew = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_orders', null=True, blank=True)

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# The following code creates the Manager and Delivery Crew groups
MANAGER_GROUP_NAME = 'Managers'
DELIVERY_CREW_GROUP_NAME = 'Delivery Crew'

def create_groups():
    manager_group, _ = Group.objects.get_or_create(name=MANAGER_GROUP_NAME)
    delivery_crew_group, _ = Group.objects.get_or_create(name=DELIVERY_CREW_GROUP_NAME)