from datetime import timezone, datetime, timedelta
from functools import reduce

from django.db.models import Q, Max
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.utils.dateparse import parse_date

from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from core.search import search_model_fulltext
from supaword import settings
from supaword.log_helper import logger
from core import models
from core.serializers import PeopleExtendedBriefSerializer, PeopleExtendedSerializer, CacheSerializer
from core.serializers import TheorySerializer
from core.requests import PagingRequestSerializer, TheoryRequestSerializer
from core.models import PeopleExtended, Theory
from core.pagination import CustomPostPagination


class SupawordAPIView(generics.CreateAPIView):
    """
    Base class for all API views
    """

    def __init__(self, request_handler):
        """
        Initialize the class
        """
        super().__init__()
        self.request_handler = request_handler
        self.http_method_names = ['post']

    @staticmethod
    def tristate_param(param):
        """
        Convert a parameter to tristate value (True, False, None)
        """
        if param is None:
            return None
        if isinstance(param, bool):
            return param
        if isinstance(param, str) and param.lower() in ['true', 'false']:
            return param.lower() == 'true'
        raise ValueError(f'Invalid tristate value [{param}]')

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

    @staticmethod
    def get_extra_actions():
        """
        Return extra actions
        :return:
        """
        return []

    def _post(self, request, *args, **kwargs):
        """
        Version of POST without exception handling
        """
        if not isinstance(request.data, dict):
            logger.error(f'Invalid request data: {request.data}')
            return Response({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

        if (request_type := request.data.get('type', '')) == '':
            logger.error(f'No request type specified in request data: {request.data}')
            return Response({'error': 'No request type specified'}, status=status.HTTP_400_BAD_REQUEST)

        if handler := self.request_handler.get(request_type):
            return handler(request)
        else:
            logger.error(f'Invalid request type: {request_type}')
            return Response({'error': 'Invalid request type'}, status=status.HTTP_400_BAD_REQUEST)

    def _post_protected(self, request, *args, **kwargs):
        """
        Version of POST with exception handling
        """
        try:
            return self._post(request, *args, **kwargs)
        except Exception as e:
            logger.error(f'Exception in _post_protected: {str(e)}')
            return Response({'Server error:': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request
        If debug mode is on, use _post method, otherwise use _post_protected
        :param request: Object of type rest_framework.request.Request
        :param args: Additional arguments
        :param kwargs: Additional keyword arguments
        :return: JSON response
        """
        if settings.DEBUG:
            return self._post(request, *args, **kwargs)
        else:
            return self._post_protected(request, *args, **kwargs)


class PeopleExtendedAPIView(SupawordAPIView):
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
        super().__init__(request_handler={
            'cache': self.return_cache,
            'page': self.return_page,
            'search': self.return_fulltext_search_result,
            'person': self.return_person_data
        })

    @staticmethod
    def return_cache(request):
        """
        Return data for caching
        """
        if request.data.get('type', '') != 'cache':
            logger.error(f'Invalid request type: {request.data.get("type", "")}')
            return Response({'error': 'Invalid request type, "cache" expected'}, status=status.HTTP_400_BAD_REQUEST)

        request_data = request.data
        logger.info(f'Cache request: {request_data}')
        created_after = request_data.get('timestamp', 0) + 1
        created_after_datetime = datetime.fromtimestamp(created_after, tz=timezone.utc)

        logger.info(f"All records created after the specified timestamp: {created_after_datetime}")
        people = PeopleExtended.objects.filter(added_on__gt=created_after_datetime).order_by('id')
        serializer = CacheSerializer(people, many=True)

        # Find the maximum value of added_on across all people
        max_added_on_result = people.aggregate(max_added_on=Max('added_on'))
        max_added_on = max_added_on_result['max_added_on']
        max_timestamp = int(max_added_on.timestamp()) if max_added_on else created_after

        response_data = {
            'cache': serializer.data,
            'timestamp': max_timestamp
        }
        return Response(response_data)

    @staticmethod
    def return_page(request):
        """
        Return paginated and filtered data
        :param request: Object of type rest_framework.request.Request
        :return: Paginated and filtered data in short JSON format
        """
        serializer = PagingRequestSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            logger.error(f'Invalid request data: {request.data}: {str(error)}')
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

        people = PeopleExtended.objects.all()
        logger.info(f'Page request: {request.data}')

        # Apply filtering
        filter_value = request.data.get('filter', '')
        age_min = request.data.get('age_min', 1)
        age_max = request.data.get('age_max', 99)
        age_min = age_min if age_min is not None else 1
        age_max = age_max if age_max is not None else 99

        sex_filter = request.data.get('sex', None)

        # Tristate filters: True, False, None
        alive_filter = SupawordAPIView.tristate_param(request.data.get('alive', None))
        traitors_filter = SupawordAPIView.tristate_param(request.data.get('is_ttu', None))
        foreign_friends_filter = SupawordAPIView.tristate_param(request.data.get('is_ff', None))

        if filter_value != '':
            people = people.filter(
                Q(fullname_en__icontains=filter_value) |
                Q(fullname_ru__icontains=filter_value) |
                Q(fullname_uk__icontains=filter_value)
            )
        people = people.filter(dod__isnull=alive_filter) if alive_filter is not None else people

        if sex_filter is not None:
            people = people.filter(sex=sex_filter)

        today = datetime.now().date()
        birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
        birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
        logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
        people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)

        if traitors_filter is not None:
            people = people.filter(is_ttu=traitors_filter)

        if foreign_friends_filter is not None:
            people = people.filter(is_ff=foreign_friends_filter)

        # Apply sorting
        sort_by = request.data.get('sort_by', 'fullname_en')
        sort_direction = request.data.get('sort_direction', 'asc')
        sort_by = f'-{sort_by}' if sort_direction == 'desc' else sort_by
        logger.info(f'Sorting condition {sort_by}')
        people = people.order_by(sort_by)

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
        logger.info(f'Search request: {request_data}')
        people = PeopleExtended.objects.filter(reduce(lambda x, y: x | y, [
            Q(fullname_en=value) |
            Q(fullname_ru=value) |
            Q(fullname_uk=value) for value in values]))
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
        logger.info(f'Fulltext search request: {request_data}')
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

        try:
            person = PeopleExtended.objects.get(id=person_id)
        except PeopleExtended.DoesNotExist:
            logger.error(f'Person with id={person_id} does not exist')
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Serialize the person and organizations data
        logger.info(f'Person data request: {request_data}')
        person_serializer = PeopleExtendedSerializer(person)
        # Combine the serialized data and return the response
        response_data = person_serializer.data
        # TODO: Serialize Organizations
        return Response(response_data)


class TheoryAPIView(SupawordAPIView):
    """
    API view to handle Theory table
    """
    queryset = models.Theory.objects.all()
    serializer_class = TheorySerializer
    parser_classes = [JSONParser]

    def __init__(self):
        """
        Initialize the class
        """
        super().__init__(request_handler={
            'general': self.return_general
        })

    @staticmethod
    def return_general(request):
        """
        Return filtered publications based on request parameters
        """
        serializer = TheoryRequestSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            logger.error(f'Invalid request data: {request.data}: {str(error)}')
            return Response({'error': f"Theory.return_general() {str(error)}"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f'General articles request: {request.data}')

        # Fetch all articles from the database and convert to a Python list
        articles = Theory.objects.all()

        sort_by = request.data.get('sort_by', 'title')
        sort_direction = request.data.get('sort_direction', 'asc')
        sort_by = f'-{sort_by}' if sort_direction == 'desc' else sort_by
        logger.info(f'Sorting condition {sort_by}')
        articles = articles.order_by(sort_by)

        serializer = TheorySerializer(articles, many=True)
        return Response(data=serializer.data)


def bad_request(request):
    """
    Return 400 Bad Request for GET requests
    """
    return HttpResponseBadRequest('<h1>400 Bad Request</h1>')
