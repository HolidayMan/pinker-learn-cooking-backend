from django.test import LiveServerTestCase
from rest_framework.test import APIClient


class ApiTest(LiveServerTestCase):
    fixtures = ["categories.json", "dishes.json", "ingredient.json", "dishingredient.json"]

    def setUp(self):
        self.client = APIClient()

    def get_json(self, url):
        """makes GET request to server_url + url"""
        return self.client.get(url).json()

    def assertNotEmpty(self, list_to_check, msg=None):
        return self.assertNotEqual(len(list_to_check), 0, msg=f"{list_to_check} is empty")

    def test_categories(self):
        # разработчик хочет получить все категории, но без доп. информации.
        # нужен просто массив словарей, в которых были бы описаны категории

        json_data = self.get_json('/api/v1/categories/all')
        self.assertNotEmpty(json_data)
        for category in json_data:
            self.assertIn("id", category, msg=f'No "id" key was found in {category}')
            self.assertIn("image_url", category, msg=f'No "image_url" key was found in {category}')
            self.assertIn("name", category, msg=f'No "name" key was found in {category}')
