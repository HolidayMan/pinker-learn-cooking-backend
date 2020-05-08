from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Category, Dish


class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Category
        fields = ['id', 'name', 'image_url']

    def get_image_url(self, obj):
        return obj.image.url


class DishSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    category = CategorySerializer()

    class Meta:
        model = Category
        fields = ['id', 'name', 'image_url', 'category']

    def get_image_url(self, obj):
        return obj.image.url


class CategoryFullSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    dishes = DishSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image_url', 'dishes']

    def get_image_url(self, obj):
        return obj.image.url
