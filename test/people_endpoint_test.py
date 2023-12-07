import unittest
from django.test import Client
from rest_framework import status
import random
import string

class PeopleExtendedApiTestCase(unittest.TestCase):
    def setUp(self):
        # Set up your test data or any other necessary setup
        self.client = Client()

    def generate_random_string(self, length=10):
        """Generate a random string of fixed length."""
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    def generate_random_data(self):
        """Generate random data for the request."""
        return {
            'type': 'page',
            'page': random.randint(0, 10),
            'page_size': random.randint(8, 120),
            'sort_by': random.choice(['id', 'fullname_en', 'fullname_ru', 'fullname_uk', 'dob', 'dod', 'sex']),
            'sort_direction': random.choice(['asc', 'desc']),
            'filter': self.generate_random_string(),
            'alive': random.choice([True, False, None]),
            'sex': random.choice(['m', 'f', None]),
            'age_min': random.randint(1, 99),
            'age_max': random.randint(1, 99),
            'is_ttu': random.choice([True, False, None]),
            'is_ff': random.choice([True, False, None]),
        }

    def test_valid_page_request(self):
        for _ in range(10):
            request_data = self.generate_random_data()
            response = self.client.post('/people', request_data, format='json')

            # Ensure the response is successful (status code 200)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Add more assertions based on your specific requirements

    def test_invalid_page_request(self):
        for _ in range(10):
            # Generate invalid data, e.g., age_min greater than age_max
            request_data = self.generate_random_data()
            request_data['age_min'] = request_data['age_max'] + 1

            response = self.client.post('/people', request_data, format='json')

            # Ensure the response is a bad request (status code 400)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            # Add more assertions based on your specific requirements for invalid requests
