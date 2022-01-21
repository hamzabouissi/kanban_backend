from rest_framework import permissions

from kanban_backend.project_management.models import Project, Sprint, Task


class IsScrumMasterPermission(permissions.BasePermission):
    # message = 'Adding customers not allowed.'

    def has_object_permission(self, request, view, obj:Project):
        if request.method in ["PATCH", "PUT"]:
            return request.user.is_authenticated and request.user == obj.scrum_master
        return True


class IsDeveloperOrScrumMasterTaskOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Task):
        if request.method in ["PATCH", "PUT"]:
            return request.user.is_authenticated and (request.user == obj.dev or request.user == obj.sprint.scrum_master)
        return True



class IsScrumMasterSprintOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Sprint):
        if request.method in ["PATCH", "PUT"]:
            return request.user.is_authenticated and  request.user == obj.scrum_master
        return True