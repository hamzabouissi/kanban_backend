from django.urls import path
from rest_framework.routers import DefaultRouter

from kanban_backend.project_management.views import ProjectViewSet, SprintViewSet, TaskViewSet


app_name = "project_management"


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'sprints', SprintViewSet, basename='sprints')


urlpatterns = [ ] + router.urls
