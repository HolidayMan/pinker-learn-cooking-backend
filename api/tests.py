from random import choice

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Ingredient, Dish, DishIngredient
from .serializers import CategorySerializer, CategoryFullSerializer, DishSerializer, DishFullSerializer, IngredientSerializer


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


class IngredientSerializerTest(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def test_ingredient_serializer(self):
        dish = choice(Dish.objects.all())
        ingredients = DishIngredient.objects.filter(dish=dish)
        json_data = IngredientSerializer(ingredients, many=True).data
        for serialized_ingredient, ingredient in zip(json_data, ingredients):
            self.assertEqual(serialized_ingredient["name"], ingredient.ingredient.name)
            self.assertEqual(serialized_ingredient["amount"], ingredient.amount)


class DishesSerializerTest(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def test_dish_serializer(self):
        model = Dish.objects.first()
        json_data = DishSerializer(model).data
        self.assertEqual(json_data["id"], model.id)
        self.assertEqual(json_data["name"], model.name)
        self.assertEqual(json_data["image_url"], model.image.url)
        self.assertEqual(json_data["category"], CategorySerializer(model.category).data)

    def test_dish_full_serializer(self):
        model = Dish.objects.first()
        json_data = DishFullSerializer(model).data
        self.assertEqual(json_data["id"], model.id)
        self.assertEqual(json_data["name"], model.name)
        self.assertEqual(json_data["image_url"], model.image.url)
        self.assertEqual(json_data["category"], CategorySerializer(model.category).data)
        self.assertEqual(json_data["ingredients"], IngredientSerializer(DishIngredient.objects.filter(dish=model), many=True).data)


class CategoriesTests(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def setUp(self):
        pass

    def check_response_status(self, url, status):
        self.assertEqual(self.client.get(url).status_code, status)

    def exact_category_tester(self, url_name, is_instance, serializer):
        category = choice(Category.objects.all())
        url = reverse(url_name, kwargs={'category_id': category.id})
        response = self.client.get(url)
        self.assertIsInstance(response.json(), is_instance)
        self.assertEqual(response.json(), serializer(category).data)

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
        self.exact_category_tester('exact-category', dict, CategorySerializer)
        self.check_response_status(reverse('exact-category', kwargs={'category_id': 100}), status.HTTP_404_NOT_FOUND)

    def test_exact_category_full(self):
        self.exact_category_tester('exact-category-full', dict, CategoryFullSerializer)
        self.check_response_status(reverse('exact-category-full', kwargs={'category_id': 100}), status.HTTP_404_NOT_FOUND)

    def test_exact_category_dishes(self):
        category = choice(Category.objects.all())
        dishes = category.dishes
        url = reverse('exact-category-dishes', kwargs={'category_id': category.id})
        response = self.client.get(url)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json(), DishFullSerializer(dishes, many=True).data)
        self.check_response_status(reverse('exact-category-dishes', kwargs={'category_id': 100}), status.HTTP_404_NOT_FOUND)


class DishesEndpointsTest(APITestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def check_response_status(self, url, status):
        self.assertEqual(self.client.get(url).status_code, status)

    def test_dishes_all(self):
        url = reverse('dishes-all')
        response = self.client.get(url)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json(), DishSerializer(Dish.objects.all(), many=True).data)
