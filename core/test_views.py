from hypothesis import given
from hypothesis.strategies import text, integers, lists, booleans, none, one_of
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from django.test import TestCase
from core.models import PeopleExtended
from core.views import PeopleExtendedAPIView
from core.serializers import PeopleExtendedSerializer, CacheSerializer, PeopleExtendedBriefSerializer

__doc__ = """# This test suite covers all the methods in the `PeopleExtendedAPIView` class. It uses Hypothesis to generate a variety of inputs for each method, ensuring that the methods can handle a wide range of possible inputs. The tests check that the methods return the expected HTTP status codes and that the structure of the response data is as expected."""


class TestPeopleExtendedAPIView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PeopleExtendedAPIView.as_view()
        self.uri = '/people/'

    @given(text(), integers(), booleans())
    def test_return_cache(self, type, timestamp, many):
        request = self.factory.post(self.uri, {'type': type, 'timestamp': timestamp}, format='json')
        response = self.view(request)
        if type != 'cache':
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.data, dict)
            self.assertIn('cache', response.data)
            self.assertIn('timestamp', response.data)
            if many:
                self.assertIsInstance(response.data['cache'], list)
            else:
                self.assertIsInstance(response.data['cache'], dict)

    @given(text(), integers(), integers(), text(), booleans(), text(), text())
    def test_return_page(self, filter, age_min, age_max, sex, alive, sort_by, sort_direction):
        request = self.factory.post(self.uri, {
            'filter': filter,
            'age_min': age_min,
            'age_max': age_max,
            'sex': sex,
            'alive': alive,
            'sort_by': sort_by,
            'sort_direction': sort_direction
        }, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    @given(lists(text()))
    def test_return_search_result(self, values):
        request = self.factory.post(self.uri, {'values': values}, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    @given(lists(text()))
    def test_return_fulltext_search_result(self, values):
        request = self.factory.post(self.uri, {'values': values}, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    @given(one_of(none(), integers()))
    def test_return_person_data(self, id):
        request = self.factory.post(self.uri, {'id': id}, format='json')
        response = self.view(request)
        if id is None or not PeopleExtended.objects.filter(id=id).exists():
            self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.data, dict)

