from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Ingredient, Dish
from .serializers import CategorySerializer


class CategoriesSerializerTest(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def test_category_all_serializer(self):
        model = Category.objects.first()
        json_data = CategorySerializer(model).data
        self.assertEqual(json_data["id"], 1)
        self.assertEqual(json_data["name"], "Напитки")
        self.assertEqual(json_data["image_url"], "/media/images/main/drinks.jpg")

        models = Category.objects.all()
        json_data = CategorySerializer(models, many=True).data
        self.assertIsInstance(json_data, list)

        for model, data in zip(models, json_data):
            self.assertEqual(data["id"], model.id)
            self.assertEqual(data["name"], model.name)
            self.assertEqual(data["image_url"], model.image.url)


class CategoriesTests(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def setUp(self):
        pass

    def test_categories_all(self):
        url = reverse('categories-all')
        response = self.client.get(url)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json(), CategorySerializer(Category.objects.all(), many=True).data)
