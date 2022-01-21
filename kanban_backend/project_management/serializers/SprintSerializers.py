


from django.contrib.auth import get_user_model
from kanban_backend.project_management.models import Sprint
from kanban_backend.users.models import Developer
from rest_framework import serializers

User = get_user_model()

class SprintInnerDeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", 'username', 'user_type')



class SprintSerializerIn(serializers.ModelSerializer):

    class Meta:
        model = Sprint
        fields = ('id','title', 'description', 'dev','project','date_start', 'date_end')



class SprintSerializerOut(serializers.ModelSerializer):

    dev = SprintInnerDeveloperSerializer()

    class Meta:
        model = Sprint
        fields = ('id','title', 'description', 'dev','project','date_start', 'date_end', "status")



class SprintSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Sprint
        fields = ('id', 'title', 'description', 'dev','project','date_start', 'date_end')