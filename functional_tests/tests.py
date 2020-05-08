from random import choice

from rest_framework import status
from django.test import LiveServerTestCase
from rest_framework.test import APIClient
from api.models import Category, Dish


class ApiTest(LiveServerTestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def setUp(self):
        self.client = APIClient()

    def get_json(self, url):
        """makes GET request to server_url + url"""

        response = self.client.get(url)
        try:
            return response.json()
        except ValueError as e:
           raise ValueError(str(e) + f". (Server returned {response.status_code})")

    def assertNotEmpty(self, list_to_check, msg=None):
        if not msg:
            return self.assertNotEqual(len(list_to_check), 0, msg=f"{list_to_check} is empty")
        else:
            return self.assertNotEqual(len(list_to_check), 0, msg=msg)

    def check_keys_in_dict(self, dictionary, *keys):
        for key in keys:
            self.assertIn(key, dictionary, msg=f'No "{key}" key was found in {dictionary}')

    def check_response_status(self, url, status):
        self.assertEqual(self.client.get(url).status_code, status)

    def test_categories_all(self):
        """testing /api/v1/categories/all"""

        # разработчик хочет получить все категории, но без доп. информации.
        # нужен просто массив словарей, в которых были бы описаны категории

        json_data = self.get_json('/api/v1/categories/all')
        self.assertNotEmpty(json_data)
        for category in json_data:
            self.check_keys_in_dict(category, 'id', 'image_url', 'name')

    def test_categories_all_full(self):
        """testing /api/v1/categories/all/full"""

        # разработчик хочет получить все категории вместе со всеми вложенными блюдами
        # нужен массив словарей с категориями и в них поле "dishes", в котором бы описывались блюда

        json_data = self.get_json('/api/v1/categories/all/full')
        self.assertNotEmpty(json_data)

        for category in json_data:
            self.check_keys_in_dict(category, 'id', 'image_url', 'name', 'dishes')

    def test_exact_category(self):
        """testing /api/v1/categories/<int>"""
        # разработчик имеет id категории и  хочет получить ссылку на её фото и название

        # получаем id категории
        # сделаем это через БД, заодно будет вся инфа о категории
        category = choice(Category.objects.all())
        category_id = category.id

        json_data = self.get_json(f'/api/v1/categories/{category_id}')
        self.assertIsInstance(json_data, dict)
        self.check_keys_in_dict(json_data, 'id', 'image_url', 'name')
        self.assertEqual(json_data.get('id'), category.id)
        self.assertEqual(json_data.get('image_url'), category.image.url)
        self.assertEqual(json_data.get('name'), category.name)

        self.check_response_status(f'/api/v1/categories/{Category.objects.count() + 10}', status.HTTP_404_NOT_FOUND)

    def test_exact_category_full(self):
        """testing /api/v1/categories/<int>/full"""

        # разработчик имеет id категории и хочет получить ссылку на её фото, название и все блюда

        # получаем id категории
        # сделаем это через БД, заодно будет вся инфа о категории
        category = choice(Category.objects.all())
        category_id = category.id

        json_data = self.get_json(f'/api/v1/categories/{category_id}/full')
        self.assertIsInstance(json_data, dict)
        self.check_keys_in_dict(json_data, 'id', 'image_url', 'name', 'dishes')
        self.assertIsInstance(json_data['dishes'], list)

        self.check_response_status(f'/api/v1/categories/{Category.objects.count() + 10}/full', status.HTTP_404_NOT_FOUND)

    def test_exact_category_dishes(self):
        """testing /api/v1/categories/<int>/dishes"""

        # разработчик имеет id категории и хочет получить её блюда

        # получаем id категории
        # сделаем это через БД, заодно будет вся инфа о категории
        category = choice(Category.objects.all())
        category_id = category.id

        json_data = self.get_json(f'/api/v1/categories/{category_id}/dishes')
        self.assertIsInstance(json_data, list)
        for dish in json_data:
            self.check_keys_in_dict(dish, 'id', 'image_url', 'name', 'category', 'ingredients')

        self.check_response_status(f'/api/v1/categories/{Category.objects.count() + 10}/dishes', status.HTTP_404_NOT_FOUND)

    def test_dishes_all(self):
        """testing /api/v1/dishes/all"""

        # разработчик хочет получить все блюда, но без доп. информации.
        # нужен просто массив словарей, в которых были бы описаны блюда

        json_data = self.get_json('/api/v1/dishes/all')
        self.assertNotEmpty(json_data)
        for dish in json_data:
            self.check_keys_in_dict(dish, 'id', 'image_url', 'name', 'category')

    def test_dishes_all_full(self):
        """testing /api/v1/dishes/all/full"""

        # разработчик хочет получить все категории вместе со всеми игридиентами
        # нужен массив словарей с блюдами и в них поле "ingredients", в котором бы описывались ингридиенты

        json_data = self.get_json('/api/v1/dishes/all/full')
        self.assertNotEmpty(json_data)

        for dish in json_data:
            self.check_keys_in_dict(dish, 'id', 'image_url', 'category', 'name', 'ingredients')

    def test_exact_dish(self):
        """testing /api/v1/dishes/<int>"""

        # разработчик имеет id блюда и хочет получить ссылку на его фото и название

        # получаем id блюда
        # сделаем это через БД, заодно будет вся инфа о блюде

        dish = choice(Dish.objects.all())
        dish_id = dish.id

        json_data = self.get_json(f'/api/v1/dishes/{dish_id}')
        self.assertIsInstance(json_data, dict)
        self.check_keys_in_dict(json_data, 'id', 'image_url', 'name', 'category')
        self.assertEqual(json_data.get('id'), dish.id)
        self.assertEqual(json_data.get('image_url'), dish.image.url)
        self.assertEqual(json_data.get('name'), dish.name)
        self.assertIsInstance(json_data.get('category'), dict)
        self.check_response_status(f'/api/v1/dishes/{Dish.objects.count() + 10}', status.HTTP_404_NOT_FOUND)

    def test_exact_dish_full(self):
        """testing /api/v1/dishes/<int>/full"""

        # разработчик имеет id блюда и хочет получить ссылку на его фото, название и ингридиенты (DishFull)

        # получаем id блюда
        # сделаем это через БД, заодно будет вся инфа о блюде

        dish = choice(Dish.objects.all())
        dish_id = dish.id

        json_data = self.get_json(f'/api/v1/dishes/{dish_id}/full')
        self.assertIsInstance(json_data, dict)
        self.check_keys_in_dict(json_data, 'id', 'image_url', 'name', 'category', 'ingredients')
        self.assertEqual(json_data.get('id'), dish.id)
        self.assertEqual(json_data.get('image_url'), dish.image.url)
        self.assertEqual(json_data.get('name'), dish.name)
        self.assertIsInstance(json_data.get('category'), dict)
        self.assertIsInstance(json_data.get('ingredients'), list)
        self.check_response_status(f'/api/v1/dishes/{Dish.objects.count() + 10}/full', status.HTTP_404_NOT_FOUND)

    def test_exact_dish_category(self):
        """testing /api/v1/dishes/<int>/category"""

        # разработчик имеет id блюда и хочет получить его категорию (Category)

        # получаем id блюда
        # сделаем это через БД, заодно будет вся инфа о блюде
        dish = choice(Dish.objects.all())
        dish_id = dish.id

        json_data = self.get_json(f'/api/v1/dishes/{dish_id}/category')
        self.assertIsInstance(json_data, dict)
        self.check_keys_in_dict(json_data, 'id', 'image_url', 'name')
        self.assertEqual(json_data.get("id"), dish.category.id)
        self.assertEqual(json_data.get("image_url"), dish.category.image.url)
        self.assertEqual(json_data.get("name"), dish.category.name)
        self.check_response_status(f'/api/v1/dishes/{Dish.objects.count() + 10}/category',
                                   status.HTTP_404_NOT_FOUND)
