from rest_framework import permissions


class CheckClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'


class CheckOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'


class CheckOwnerStoreEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class CheckOwnerProductEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.store.owner
