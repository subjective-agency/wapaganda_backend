from datetime import timezone, datetime
from functools import reduce

from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.conf import settings

from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from core.search import search_model_fulltext
from supaword import settings
from core import models
from core.serializers import PeopleExtendedBriefSerializer, CacheSerializer, PeopleExtendedSerializer
from core.serializers import OrganizationSerializer
from core.serializers import TheorySerializer
from core.serializers import PagingRequestSerializer
from core.models import PeopleExtended, PeopleInOrgs, Organizations, Theory
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
            return Response({'error': 'Invalid request type, "cache" expected'}, status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        created_after = request_data.get('timestamp', 0)
        created_after_datetime = datetime.fromtimestamp(created_after, tz=timezone.utc)

        # All records created after the specified timestamp
        if settings.DEBUG:
            people = PeopleExtended.objects.filter(added_on__gt=created_after_datetime).order_by('id')[:20]
        else:
            people = PeopleExtended.objects.filter(added_on__gt=created_after_datetime).order_by('id')

        serializer = CacheSerializer(people, many=True)
        return Response(data=serializer.data)

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
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

        people = PeopleExtended.objects.all()

        # Apply filtering
        filter_value = request.data.get('filter', '')
        alive_filter = SupawordAPIView.tristate_param(request.data.get('alive', None))

        if filter_value != '':
            people = people.filter(
                Q(fullname_en__icontains=filter_value) |
                Q(fullname_ru__icontains=filter_value) |
                Q(fullname_uk__icontains=filter_value)
            )
        people = people.filter(dod__isnull=alive_filter) if alive_filter is not None else people

        # Apply sorting
        sort_by = request.data.get('sort_by', 'fullname_en')
        sort_direction = request.data.get('sort_direction', 'asc')
        sort_by = f'-{sort_by}' if sort_direction == 'desc' else sort_by
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
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Serialize the person and organizations data
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
            'all': self.return_all
        })

    @staticmethod
    def return_all(request):
        """
        Return all publications
        """
        if request.data.get('type', '') != 'all':
            return Response({'error': 'Invalid request type, "cache" expected'}, status=status.HTTP_400_BAD_REQUEST)
        theory = Theory.objects.all()
        sort_by = request.data.get('sort_by', 'title')
        sort_direction = request.data.get('sort_direction', 'asc')
        sort_by = f'-{sort_by}' if sort_direction == 'desc' else sort_by
        theory = theory.order_by(sort_by)
        serializer = TheorySerializer(theory, many=True)
        return Response(data=serializer.data)


class OrganizationsAPIView(SupawordAPIView):
    """
    API view to handle Organizations
    """
    queryset = models.Organizations.objects.all()
    serializer_class = OrganizationSerializer
    parser_classes = [JSONParser]
    pagination_class = CustomPostPagination

    def __init__(self):
        """
        Initialize the class
        """
        super().__init__(request_handler={
            'all': self.return_all_organizations,
            'person': self.person_organization_data
        })

    @staticmethod
    def return_all_organizations(request):
        """
        :param request:
        :return:
        """
        organizations = Organizations.objects.all().order_by('id')[:20]
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(data=serializer.data)

    @staticmethod
    def person_organization_data(request):
        request_data = request.data
        person_id = request_data.get('id')

        # Get all the organization IDs where the person is registered
        orgs = PeopleInOrgs.objects.filter(person=person_id)
        orgs_ids = [org.id for org in orgs]

        # Get all the organizations with the IDs
        organizations = Organizations.objects.filter(id__in=orgs_ids)
        organizations_serializer = OrganizationSerializer(organizations, many=True)

        return Response(data=organizations_serializer.data)


def bad_request(request):
    """
    Return 400 Bad Request for GET requests
    """
    return HttpResponseBadRequest('<h1>400 Bad Request</h1>')
