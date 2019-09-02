import unittest
import os
import requests
import re

class TestService(unittest.TestCase):
    url = os.getenv('SERVICE_URL', 'http://127.0.0.1:8890')

    def test_response_format(self):
        for attempt in range(10):
            response = requests.get(self.url, timeout=1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.encoding, 'utf-8')
            self.assertTrue(re.match('^\w+ is \d+ years$', response.text))

if __name__ == '__main__':
    unittest.main()
