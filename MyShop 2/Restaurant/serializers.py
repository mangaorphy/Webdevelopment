from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Order, Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category', 'is_item_of_the_day']

class CartSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True)
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'menu_items', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    customer = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    cart = CartSerializer(source='cart_set', read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'menu_items', 'order_date', 'is_delivered', 'delivery_crew', 'cart']