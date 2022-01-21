from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from kanban_backend.project_management.models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status","date_start", "date_end")


class UserSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username", "name","user_type"]



class UserSerializerIn(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id","username", "name", "email", "user_type", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        return make_password(value)



class UserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        return make_password(value)


class UserWithTaskSerializerList(serializers.ModelSerializer):
   
    my_tasks = TaskSerializer(many=True)
    class Meta:
        model = User
        fields = ["id","username", "name", "email","my_tasks"]