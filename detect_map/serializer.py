from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'password']



