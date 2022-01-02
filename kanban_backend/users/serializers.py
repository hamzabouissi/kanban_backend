from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

User = get_user_model()


class UserSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name","user_type"]




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