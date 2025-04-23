
import re, json
from rest_framework import serializers




from .models import User,UserRole


from app.serializers.branch import BrachNameSerializer


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = "__all__"


class RequestUserSerializer(serializers.ModelSerializer):
    user_role = UserRoleSerializer()
    branch = BrachNameSerializer(many = True,required = False) 

    class Meta:
        model = User
        fields = (
            "id",
            "user_role",
            "phone_number",
            "branch",
            "full_name",
            "email",
            "address",
            "avatar"
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email","address","branch","user_role","full_name","phone_number","avatar")
