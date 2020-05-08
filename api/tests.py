from random import choice

from django.urls import reverse

from rest_framework.test import APITestCase
from .models import Category, Ingredient, Dish
from .serializers import CategorySerializer, CategoryFullSerializer, DishSerializer


class CategoriesSerializersTest(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def test_category_serializer(self):
        # testing one model object

        model = Category.objects.first()
        json_data = CategorySerializer(model).data
        self.assertEqual(json_data["id"], model.id)
        self.assertEqual(json_data["name"], model.name)
        self.assertEqual(json_data["image_url"], model.image.url)

        # testing many model objects

        models = Category.objects.all()
        json_data = CategorySerializer(models, many=True).data
        self.assertIsInstance(json_data, list)

        for model, data in zip(models, json_data):
            self.assertEqual(data["id"], model.id)
            self.assertEqual(data["name"], model.name)
            self.assertEqual(data["image_url"], model.image.url)

    def test_category_full_serializer(self):
        # testing one model object

        model = Category.objects.first()
        json_data = CategoryFullSerializer(model).data
        self.assertEqual(json_data["id"], model.id)
        self.assertEqual(json_data["name"], model.name)
        self.assertEqual(json_data["image_url"], model.image.url)
        self.assertIn("dishes", json_data)


class DishesSerializerTest(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def test_dish_serializer(self):
        model = Dish.objects.first()
        json_data = DishSerializer(model).data
        self.assertEqual(json_data["id"], model.id)
        self.assertEqual(json_data["name"], model.name)
        self.assertEqual(json_data["image_url"], model.image.url)
        self.assertEqual(json_data["category"], CategorySerializer(model.category).data)


class CategoriesTests(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def setUp(self):
        pass

    def test_categories_all(self):
        url = reverse('categories-all')
        response = self.client.get(url)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json(), CategorySerializer(Category.objects.all(), many=True).data)

    def test_categories_all_full(self):
        url = reverse('categories-all-full')
        response = self.client.get(url)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json(), CategoryFullSerializer(Category.objects.all(), many=True).data)

    def test_exact_category(self):
        category = choice(Category.objects.all())
        url = reverse('exact-category', kwargs={'category_id': category.id})
        response = self.client.get(url)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json(), CategorySerializer(category).data)
