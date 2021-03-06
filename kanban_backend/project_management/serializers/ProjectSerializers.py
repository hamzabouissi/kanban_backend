


from kanban_backend.project_management.models import Project
from kanban_backend.users.models import Developer
from rest_framework import serializers



class ProjectInnerDeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = ("id",)



class ProjectSerializerIn(serializers.ModelSerializer):
    scrum_master = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Project
        fields = ('id','title','description', 'owner', 'scrum_master','date_start', 'date_end')



class ProjectSerializerOut(serializers.ModelSerializer):

    developers = ProjectInnerDeveloperSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id','title','description', 'owner', 'scrum_master', 'developers', 'date_start', 'date_end')



class ProjectSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('title','description','owner', 'scrum_master', 'date_start', 'date_end')