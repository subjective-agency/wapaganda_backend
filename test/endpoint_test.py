import os
import unittest
from django.test import Client
from rest_framework import status
import random
import string


__doc__ = """In the integration test we are using `random` 
to generate random POST request payloads.
TODO: Maximum number of pages comes from database
"""


class PeopleExtendedApiTestCase(unittest.TestCase):
    """
    Endpoint example:
    https://wapaganda-backend-development.up.railway.app/people/
    """
    def setUp(self):
        """
        Set up your test data or any other necessary setup
        """
        self.client = Client()
        os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'wapaganda-backend-development.up.railway.app'

    @staticmethod
    def generate_random_string(length=10):
        """
        Generate a random string of fixed length
        """
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    def max_page():
        return 50

    def generate_random_data(self):
        """
        Generate random data for the request
        """
        return {
            'type': 'page',
            'page': random.randint(0, 10),
            'page_size': random.randint(10, 20),
            'sort_by': random.choice(['id', 'fullname', 'dob', 'dod', 'sex']),
            'sort_direction': random.choice(['asc', 'desc']),
            'filter': self.generate_random_string(),
            'alive': random.choice([True, False]),
            'sex': random.choice(['m', 'f']),
            'age_min': random.randint(1, 99),
            'age_max': random.randint(1, 99),
            # 'is_ttu': random.choice([True, False]),
            # 'is_ff': random.choice([True, False]),
        }

    def generate_simple_data(self):
        """
        Generate simplest request
        """
        return {
            'type': 'page',
            'page': random.randint(0, self.max_page()),
            'page_size': random.randint(10, 20)
        }

    @staticmethod
    def print_request(url, method, request_data):
        print(f"\n\nRequest: {method} {url}")
        print(f"Request Data: {request_data}")

    @staticmethod
    def print_response(response):
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Data: {response.data}\n\n")

    def test_valid_page_request(self):
        """
        10 valid requests
        """
        for _ in range(10):
            request_data = self.generate_simple_data()
            response = self.client.post('/people', request_data, format='json')

            # Full URL
            host = os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS', 'localhost:8000')
            full_url = f"https://{host}{response.url}"
            print(f"Full URL: {full_url}")

            # Ensure the response is successful (status code 200)
            # Add more assertions based on your specific requirements
            self.print_request(url=full_url, method='POST', request_data=request_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.print_response(response=response)
