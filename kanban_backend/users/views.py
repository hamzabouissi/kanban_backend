from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from kanban_backend.base.BaseSerializers import SerializerNone

from .serializers import  UserSerializerIn, UserSerializerOut, UserSerializerUpdate

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializers_class = {
        "list": UserSerializerOut,
        "retrieve": UserSerializerOut,
        "create": UserSerializerIn,
        "update": UserSerializerUpdate
    }
    queryset = User.objects.all()
    lookup_field = "username"


    def get_serializer_class(self):
        return self.serializers_class.get(self.action,SerializerNone)

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = self.get_serializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

   
