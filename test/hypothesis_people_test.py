from hypothesis import given, strategies as st
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

__doc__ = """In this example, we are using Hypothesis to generate random dictionaries 
with keys of type string and values of type integer. 
These dictionaries are used as the data for the POST request. 
The `given` decorator is used to specify the input data for the test.
Remember to run your tests with a command like `python manage.py test`.
"""


class PeopleExtendedApiTestCase(TestCase):

    @given(st.dictionaries(
        keys=st.sampled_from(['type',
                              'page',
                              'page_size',
                              'sort_by',
                              'sort_direction',
                              'filter',
                              'alive',
                              'sex',
                              'age_min',
                              'age_max',
                              'is_ttu',
                              'is_ff']),
        values=st.one_of(
            st.none(),
            # age values between 1 and 99
            st.integers(min_value=1, max_value=99),
            # predefined fullnames
            st.sampled_from(["Ivan*", "Andrey*", "Svetlana*"]),
            # True/False values for alive, is_ttu, is_ff
            st.booleans()
        )
    ))
    def test_valid_page_request(self, request_data):
        client = APIClient()
        for _ in range(10):
            response = client.post('/people', request_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    @given(st.dictionaries(
        keys=st.sampled_from(['type',
                              'page',
                              'page_size',
                              'sort_by',
                              'sort_direction',
                              'filter',
                              'alive',
                              'sex',
                              'age_min',
                              'age_max',
                              'is_ttu',
                              'is_ff']),
        values=st.one_of(
            st.none(),
            # age values greater than 99 (invalid)
            st.integers(min_value=100),
            # any text for filter
            st.text(),
            # True/False values for alive, is_ttu, is_ff
            st.booleans()
        )
    ))
    def test_invalid_page_request(self, request_data):
        client = APIClient()
        for _ in range(10):
            response = client.post('/people', request_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
