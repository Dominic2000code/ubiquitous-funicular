from rest_framework import permissions


class IsGroupCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
