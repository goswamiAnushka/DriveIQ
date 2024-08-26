# tests/test_api.py
import unittest
import json
from src.app import app

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict(self):
        response = self.app.post('/predict', 
                                 data=json.dumps({
                                     'avg_speed': 65,
                                     'max_acceleration': 1.2,
                                     'total_heading_change': 15
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('predicted_behavior', data)

if __name__ == '__main__':
    unittest.main()
