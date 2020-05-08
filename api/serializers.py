from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Category, Dish, DishIngredient


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
        model = Dish
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


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_ingredient_name')

    class Meta:
        model = DishIngredient
        fields = ['name', 'amount']

    def get_ingredient_name(self, obj):
        return obj.ingredient.name


class DishFullSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    ingredients = serializers.SerializerMethodField('get_ingredients')
    category = CategorySerializer()

    class Meta:
        model = Dish
        fields = ['id', 'name', 'image_url', 'category', 'ingredients']

    def get_ingredients(self, obj):
        return IngredientSerializer(DishIngredient.objects.filter(dish=obj), many=True).data

    def get_image_url(self, obj):
        return obj.image.url
