


from kanban_backend.project_management.models import Sprint
from kanban_backend.users.models import Developer
from rest_framework import serializers



class SprintInnerDeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = ("id",)



class SprintSerializerIn(serializers.ModelSerializer):

    class Meta:
        model = Sprint
        fields = ('id', 'description', 'dev','project','date_start', 'date_end')



class SprintSerializerOut(serializers.ModelSerializer):

    dev = SprintInnerDeveloperSerializer()

    class Meta:
        model = Sprint
        fields = ('id', 'description', 'dev','project','date_start', 'date_end')



class SprintSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Sprint
        fields = ('id', 'description', 'dev','project','date_start', 'date_end')