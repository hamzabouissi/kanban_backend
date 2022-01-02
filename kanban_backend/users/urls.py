from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings
from kanban_backend.users.views import UserViewSet

app_name = "users"

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
