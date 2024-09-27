# core/serializers.py

from rest_framework import serializers
from .models import UserDetail

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['email', 'username', 'password', 'mob_no', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserDetail(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
