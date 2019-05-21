from service_api.manage import app
import json
import unittest


class AutoRestTests(unittest.TestCase):

    def test_get_metrics_all(self):
        request, response = app.test_client.get('/')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data['message'], 'Hello world!')


if __name__ == '__main__':
    unittest.main()
