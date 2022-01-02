from rest_framework import permissions


class IsScrumMasterPermission(permissions.BasePermission):
    # message = 'Adding customers not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT"]:
            return request.user.is_authenticated and request.user == obj.scrum_master
        return True


class IsDeveloperTaskOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT"]:
            return request.user.is_authenticated and request.user == obj.dev
        return True
