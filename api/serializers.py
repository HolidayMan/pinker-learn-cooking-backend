from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']
