from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from kanban_backend.base.BaseSerializers import SerializerNone

from kanban_backend.project_management.models import Project, Sprint, Task
from kanban_backend.project_management.permissions import IsDeveloperOrScrumMasterTaskOwner, IsScrumMasterPermission, IsScrumMasterSprintOwner
from kanban_backend.project_management.serializers.ProjectSerializers import ProjectSerializerIn, ProjectSerializerOut, ProjectSerializerUpdate
from kanban_backend.project_management.serializers.SprintSerializers import SprintSerializerIn, SprintSerializerOut, SprintSerializerUpdate
from kanban_backend.project_management.serializers.TaskSerializers import TaskSerializerIn, TaskSerializerOut, TaskSerializerUpdate, TaskSerializerUpdateDev
# Create your views here.

User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializers_class = {
        "list": ProjectSerializerOut,
        "retrieve":ProjectSerializerOut,
        "create": ProjectSerializerIn,
        "update": ProjectSerializerUpdate
    }
    permission_classes = (IsScrumMasterPermission,)


    def get_serializer_class(self):
        return self.serializers_class.get(self.action,SerializerNone)




class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializers_class = {
        "list": SprintSerializerOut,
        "retrieve":SprintSerializerOut,
        "create": SprintSerializerIn,
        "update": SprintSerializerUpdate
    }
    permission_classes = (IsScrumMasterSprintOwner,)


    def get_serializer_class(self):
        return self.serializers_class.get(self.action,SerializerNone)



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializers_class = {
        "list": TaskSerializerOut,
        "retrieve":TaskSerializerOut,
        "create": TaskSerializerIn,
        "update": TaskSerializerUpdate,
        "partial_update": TaskSerializerUpdate,
        "change_developer": TaskSerializerUpdateDev
    }
    permission_classes = (IsDeveloperOrScrumMasterTaskOwner,)


    def get_serializer_class(self):
        return self.serializers_class.get(self.action,SerializerNone)


    @action(detail=True, methods=["POST"])
    def change_developer(self,request, *args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        developer_id = serializer.data.get("dev")
        dev = User.objects.get(id=developer_id)
        task:Task = self.get_object()
        task.change_dev(dev)
        return Response(status=status.HTTP_204_NO_CONTENT)