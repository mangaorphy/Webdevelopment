from rest_framework import permissions
from .models import MANAGER_GROUP_NAME, DELIVERY_CREW_GROUP_NAME

class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name=MANAGER_GROUP_NAME).exists()

class IsDeliveryCrew(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.delivery_crew == request.user or request.user.groups.filter(name=DELIVERY_CREW_GROUP_NAME).exists()