from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Ingredient, Dish


class CategoriesTests(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def setUp(self):
        pass

    def test_categories_all(self):
        url = reverse('categories-all')
        response = self.client.get(url)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json(), CategorySerializer(Category.objects.all(), many=True).data)

