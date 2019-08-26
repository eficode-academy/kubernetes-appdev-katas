import unittest
import os
import requests
import re

class TestAge(unittest.TestCase):
    url = os.getenv('SERVICE_URL', 'http://127.0.0.1:8888')

    def test_response_format(self):
        response = requests.get(self.url, timeout=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.encoding, 'utf-8')
        self.assertTrue(re.match('^\d+$', response.text))

    def test_range(self):
        response = requests.get(self.url, timeout=1)
        age = int(response.text)
        self.assertTrue(age>0)
        self.assertTrue(age<100)

if __name__ == '__main__':
    unittest.main()
