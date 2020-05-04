from django.test import LiveServerTestCase
import requests


class ApiTest(LiveServerTestCase):
    def get_json(self, url):
        """makes GET request to server_url + url"""
        return requests.get(self.live_server_url + url).json()

    def assertNotEmpty(self, list_to_check, msg=None):
        return self.assertNotEqual(len(list_to_check), 0)

    def test_categories(self):
        # разработчик хочет получить все категории, но без доп. информации.
        # нужен просто массив словарей, в которых были бы описаны категории

        json_data = self.get_json('/categories/all')
        self.assertNotEmpty(json_data)
        for category in json_data:
            self.assertIn("id", category, msg=f'No "id" key was found in {category}')
            self.assertIn("image_url", category, msg=f'No "image_url" key was found in {category}')
            self.assertIn("name", category, msg=f'No "name" key was found in {category}')
