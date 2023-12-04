from hypothesis import given
from hypothesis.strategies import integers, dictionaries, text
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request
from .pagination import CustomPostPagination
from .views import YourViewSet  # TODO?
from .models import YourModel  # TODO?
from django.test import TestCase

# In this example, we are using Hypothesis to generate random dictionaries with keys of type string and values of type integer. These dictionaries are used as the data for the POST request. The `given` decorator is used to specify the input data for the test.
#
# Please replace `YourViewSet` and `YourModel` with the actual ViewSet and Model you are using in your project. Also, replace `/api/your_endpoint/` with the actual endpoint you are testing.
#
# Remember to run your tests with a command like `python manage.py test`.

class TestCustomPostPagination(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = YourViewSet.as_view({'post': 'list'})
        self.pagination = CustomPostPagination()
        self.user = YourModel.objects.create_user('test', 'test@test.com', 'test')

    @given(dictionaries(text(min_size=5, max_size=20), integers(min_value=1, max_value=100)))
    def test_get_page_number(self, data):
        request = self.factory.post('/api/your_endpoint/', data, format='json')
        force_authenticate(request, user=self.user)
        request = Request(request)
        page_number = self.pagination.get_page_number(request, self.pagination)
        self.assertTrue(isinstance(page_number, int))
        self.assertTrue(page_number >= 1)

    @given(dictionaries(text(min_size=5, max_size=20), integers(min_value=1, max_value=100)))
    def test_get_page_size(self, data):
        request = self.factory.post('/api/your_endpoint/', data, format='json')
        force_authenticate(request, user=self.user)
        request = Request(request)
        page_size = self.pagination.get_page_size(request)
        self.assertTrue(isinstance(page_size, int))
        self.assertTrue(self.pagination.min_page_size <= page_size <= self.pagination.max_page_size)

