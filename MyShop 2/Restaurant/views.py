from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Category, MenuItem, Order, Cart
from .serializers import UserSerializer, CategorySerializer, MenuItemSerializer, OrderSerializer, CartSerializer
from .permissions import IsManagerOrReadOnly, IsDeliveryCrew

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def assign_to_manager(self, request, pk=None):
        user = self.get_object()
        manager_group = Group.objects.get(name=MANAGER_GROUP_NAME)
        user.groups.add(manager_group)
        return Response({'message': 'User assigned to manager group'})

    @action(detail=True, methods=['post'])
    def assign_to_delivery_crew(self, request, pk=None):
        user = self.get_object()
        delivery_crew_group = Group.objects.get(name=DELIVERY_CREW_GROUP_NAME)
        user.groups.add(delivery_crew_group)
        return Response({'message': 'User assigned to delivery crew group'})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrReadOnly]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]

    @action(detail=True, methods=['post'])
    def set_item_of_the_day(self, request, pk=None):
        item = self.get_object()
        item.is_item_of_the_day = True
        item.save()
        return Response({'message': 'Item set as item of the day'})

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsDeliveryCrew()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        cart = self.request.user.cart_set.last()
        serializer.save(customer=self.request.user, menu_items=cart.menu_items.all())
        cart.delete()