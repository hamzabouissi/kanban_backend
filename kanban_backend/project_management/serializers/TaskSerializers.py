


from kanban_backend.project_management.models import Task
from kanban_backend.users.models import Developer
from rest_framework import serializers



class TaskInnerDeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = ("id",)



class TaskSerializerIn(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id','title', 'description', 'dev', 'sprint', 'status', 'date_start', 'date_end')



class TaskSerializerOut(serializers.ModelSerializer):

    dev = TaskInnerDeveloperSerializer()

    class Meta:
        model = Task
        fields = ('id','title', 'description', 'dev','sprint', 'status', 'date_start', 'date_end')



class TaskSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id','title', 'description', 'sprint', 'status', 'date_start', 'date_end')





class TaskSerializerUpdateDev(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'dev')