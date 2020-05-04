from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Category
        fields = ['id', 'name', 'image_url']

    def get_image_url(self, obj):
        return obj.image.url
