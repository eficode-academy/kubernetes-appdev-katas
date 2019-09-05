#!/usr/bin/env python

import unittest
import os
import requests
import re

class TestName(unittest.TestCase):
    url = os.getenv('SERVICE_URL', 'http://127.0.0.1:8889')

    def test_response_format(self):
        response = requests.get(self.url, timeout=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.encoding, 'utf-8')
        self.assertTrue(re.match('^[A-Z]{1}[a-z]+$', response.text))

if __name__ == '__main__':
    unittest.main()
