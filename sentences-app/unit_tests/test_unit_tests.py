#!/usr/bin/env python

import unittest
import re
import random

import app.utils as app

class TestNameUnittest(unittest.TestCase):
    def test_response_format(self):
        random.seed(0)
        for attempt in range(10):
            name = app.get_random_name()
            self.assertTrue(re.match('^[A-Z]{1}[a-z]+$', name))

if __name__ == '__main__':
    unittest.main()
