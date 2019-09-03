#!/usr/bin/env python

import unittest
import re
import random

import app.utils as app

class TestNameUnittest(unittest.TestCase):
    def test_name_casing(self):
        random.seed(0)
        for attempt in range(10):
            name = app.get_random_name()
            self.assertTrue(re.match('^[A-Z]{1}[a-z]+$', name))

    def test_name_length(self):
        random.seed(0)
        for attempt in range(10):
            name = app.get_random_name()
            self.assertTrue(len(name) < 20)

    def test_randomness_distribution(self):
        random.seed(0)
        got_name = {}
        for attempt in range(100):
            name = app.get_random_name()
            got_name[name] = got_name.get(name, 0)+1
        self.assertTrue(len(got_name.keys()) > 0) # Expect between 1 and 5 names
        self.assertTrue(len(got_name.keys()) < 6)

if __name__ == '__main__':
    unittest.main()
