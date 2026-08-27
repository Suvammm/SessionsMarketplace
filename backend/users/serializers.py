from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'role', 'role_selected', 'bio', 'date_joined')
        read_only_fields = ('id', 'email', 'role', 'role_selected', 'date_joined')

class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()

class PasswordLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)

class RoleSelectionSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=[User.Role.USER, User.Role.CREATOR])
