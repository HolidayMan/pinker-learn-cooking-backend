from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Ingredient, Dish


class CategoriesTests(APITestCase):
    def setUp(self):
        pass

    def test_categories_all(self):
        url = reverse('categories-all')
        response = self.client.get(url)
        self.assertIsInstance(response, list)
        # self.asse

