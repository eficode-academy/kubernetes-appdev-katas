#!/usr/bin/env python

import unittest
import os
import requests
import re
from prometheus_client.parser import text_string_to_metric_families

class TestAge(unittest.TestCase):
    url = os.getenv('SERVICE_URL', 'http://127.0.0.1:8888')
    metrics_url = os.getenv('METRICS_URL', 'http://127.0.0.1:8000')

    def get_metric(self, metric_name):
        metrics = requests.get(self.metrics_url, timeout=1).content
        for family in text_string_to_metric_families(metrics):
            if family.samples[0][0]==metric_name:
                return [(sample[2], sample[1]) for sample in family.samples]

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

    def test_request_metric(self):
        m1 = self.get_metric('sentence_requests_total')
        self.assertTrue(len(m1)==1)
        self.assertTrue(set(m1[0][1].keys())==set(['type']))
        self.assertTrue(m1[0][1]['type']=='age')
        cnt1 = m1[0][0]
        response = requests.get(self.url, timeout=1)
        m2 = self.get_metric('sentence_requests_total')
        self.assertTrue(len(m2)==1)
        self.assertTrue(set(m2[0][1].keys())==set(['type']))
        self.assertTrue(m1[0][1]['type']=='age')
        self.assertTrue(m2[0][0]==cnt1+1)

if __name__ == '__main__':
    unittest.main()
