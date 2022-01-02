from rest_framework import viewsets
from kanban_backend.base.BaseSerializers import SerializerNone

from kanban_backend.project_management.models import Project, Sprint, Task
from kanban_backend.project_management.permissions import IsDeveloperTaskOwner, IsScrumMasterPermission
from kanban_backend.project_management.serializers.ProjectSerializers import ProjectSerializerIn, ProjectSerializerOut, ProjectSerializerUpdate
from kanban_backend.project_management.serializers.SprintSerializers import SprintSerializerIn, SprintSerializerOut, SprintSerializerUpdate
from kanban_backend.project_management.serializers.TaskSerializers import TaskSerializerIn, TaskSerializerOut, TaskSerializerUpdate
# Create your views here.


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


    def get_serializer_class(self):
        return self.serializers_class.get(self.action,SerializerNone)



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializers_class = {
        "list": TaskSerializerOut,
        "retrieve":TaskSerializerOut,
        "create": TaskSerializerIn,
        "update": TaskSerializerUpdate
    }
    permission_classes = (IsDeveloperTaskOwner,)


    def get_serializer_class(self):
        return self.serializers_class.get(self.action,SerializerNone)