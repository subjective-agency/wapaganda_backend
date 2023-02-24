from functools import reduce

from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from supaword import settings
from core import models
from core.serializers import PeopleExtendedBriefSerializer, PeopleExtendedSerializer
from core.models import PeopleExtended
from core.pagination import CustomPostPagination


def search_model_fulltext(model, fields: list, values: list):
    """
    Perform full-text search on a Django model.
    :param model: The Django model to search.
    :param fields: List of field names to search.
    :param values: List of search query values.
    :return: QuerySet of objects matching the search query.
    """
    search_queries = [
        Q(**{f'{field}__icontains': value}) for value in values
        for field in fields
    ]
    results = model.objects.filter(reduce(lambda a, b: a | b, search_queries))
    return results


class PeopleExtendedAPIView(generics.CreateAPIView):
    """
    API view to handle PeopleExtended data
    """
    queryset = models.PeopleExtended.objects.all()
    serializer_class = PeopleExtendedSerializer
    parser_classes = [JSONParser]
    pagination_class = CustomPostPagination

    def __init__(self):
        """
        Initialize the class
        """
        super().__init__()
        self.request_handler = {
            'all': self.return_all_data,
            'page': self.return_page,
            'search': self.return_fulltext_search_result,
            'person': self.return_person_data
        }

    @staticmethod
    def return_all_data(_):
        """
        Return all data
        :param _: Object of type rest_framework.request.Request
        :return: All the data in short JSON format
        """
        # In DEBUG mode we return only 20 records for test purposes
        if settings.DEBUG:
            people = PeopleExtended.objects.all().order_by('id')[:20]
        else:
            people = PeopleExtended.objects.all().order_by('id')
        serializer = PeopleExtendedBriefSerializer(people, many=True)
        return Response(data=serializer.data, headers={'Server-Version': settings.VERSION})

    @staticmethod
    def return_page(request):
        """
        Return all data
        :param request: Object of type rest_framework.request.Request
        :return: All the data in short JSON format
        """
        if request.data.get('type', '') != 'page':
            return Response({'error': 'Invalid request type, "page" expected'}, status=status.HTTP_400_BAD_REQUEST)

        people = PeopleExtended.objects.all().order_by('id')
        paginator = CustomPostPagination()
        result_page = paginator.paginate_queryset(people, request)
        serializer = PeopleExtendedBriefSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @staticmethod
    def return_search_result(request):
        """
        Return search result
        :param request: Object of type rest_framework.request.Request
        :return: JSON response
        """
        request_data = request.data
        values = request_data.get('values', [])
        print(f'Values: {values}')
        people = PeopleExtended.objects.filter(reduce(lambda x, y: x | y, [
            Q(fullname_en=value) | Q(fullname_ru=value) | Q(fullname_uk=value) for value in values]))
        serializer = PeopleExtendedBriefSerializer(people, many=True)
        return Response(serializer.data)

    @staticmethod
    def return_fulltext_search_result(request):
        """
        Return fulltext search result
        :param request: Object of type rest_framework.request.Request
        :return: JSON response
        """
        request_data = request.data
        values = request_data.get('values', [])

        people = search_model_fulltext(model=PeopleExtended,
                                       fields=['fullname_en', 'fullname_ru', 'fullname_uk'],
                                       values=values)

        serializer = PeopleExtendedBriefSerializer(people, many=True)
        return Response(serializer.data)

    @staticmethod
    def return_person_data(request):
        """
        Return person data
        :param request: Object of type rest_framework.request.Request
        :return: JSON response full data of the person
        """
        request_data = request.data
        person_id = request_data.get('id')
        people = PeopleExtended.objects.filter(id=person_id)
        serializer = PeopleExtendedSerializer(people, many=True)
        return Response(serializer.data)

    def _post(self, request, *args, **kwargs):
        """
        Version of POST without exception handling
        """
        if not isinstance(request.data, dict):
            return Response({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

        if (request_type := request.data.get('type', '')) == '':
            return Response({'error': 'No request type specified'}, status=status.HTTP_400_BAD_REQUEST)

        if handler := self.request_handler.get(request_type):
            return handler(request)
        else:
            return Response({'error': 'Invalid request type'}, status=status.HTTP_400_BAD_REQUEST)

    def _post_protected(self, request, *args, **kwargs):
        """
        Version of POST with exception handling
        """
        try:
            return self._post(request, *args, **kwargs)
        except Exception as e:
            return Response({'Server error:': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request
        If debug mode is on, use debug_post
        :param request: Object of type rest_framework.request.Request
        :param args: Additional arguments
        :param kwargs: Additional keyword arguments
        :return: JSON response
        """
        if settings.DEBUG:
            return self._post(request, *args, **kwargs)
        else:
            return self._post_protected(request, *args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Check request type and allow only POST
        """
        if request.method != 'POST':
            return Response({'error': 'Invalid access method'}, status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request, *args, **kwargs)
