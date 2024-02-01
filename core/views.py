from datetime import timezone, datetime, timedelta
from functools import reduce
from enum import Enum

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
from wganda import settings
from wganda.log_helper import logger
from core.serializers import PeopleExtendedBriefSerializer, PeopleExtendedSerializer, CacheSerializer, BundleSerializer, TheorySerializer
from core.requests import PagingRequestSerializer, TheoryRequestSerializer
from core.models import PeopleExtended, Theory, PeopleBundles
from core.models import PeopleOnSmotrim, PeopleOnYoutube, MediaSegments, YoutubeVids, SmotrimEpisodes, MediaRoles
from core.pagination import CustomPostPagination


class BundleType(Enum):
    ExpertBundles = 1
    FlagsBundles = 3
    GroupsBundles = 4


class WAPIView(generics.CreateAPIView):
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


class AirtimeAPIView(WAPIView):
    """
    API view to shape data related to patient's appearances on air
    """
    serializer_class = AirtimeSerializer
    parser_classes = [JSONParser]

    def __init__(self):
        super().__init__(request_handler={
            'on_smotrim': self.collect_smotrim,
            'on_youtube': self.collect_youtube
        })

    @staticmethod
    def collect_smotrim(request):
        queryset = PeopleOnSmotrim.objects.filter(person_id=request.data["person_id"])
        episodes = []
        for query in queryset:
            role_data = MediaRoles.objects.filter(id=query.role_id).first()
            episode_data = SmotrimEpisodes.objects.filter(id=query.episode_id).first()
            segment_data = MediaSegments.objects.filter(id=episode_data.segment_id).first()
            obj = {
                "episode_id": query.episode_id,
                "episode_title": episode_data.title,
                "episode_duration": episode_data.duration,
                "episode_date": episode_data.timestamp_aired,
                "media_segment_id": episode_data.media_segment_id,
                "media_segment_name": segment_data.name,
                "role": role_data.role,
            }
            episodes.append(obj)
        serialized = AirtimeSerializer(episodes, many=True)

        return Response(data={
            "total": {
                "appearances_count": len(episodes),
                "roles": list(set([x.get("role") for x in episodes])),
                # "segments": list(set([x.get("media_segment_name") for x in serialized]))
            },
            "episodes": serialized
        })

    @staticmethod
    def collect_youtube(self):
        queryset = PeopleOnYoutube.objects.filter(person_id=request.data["person_id"])
        episodes = []
        for query in queryset:
            role_data = MediaRoles.objects.filter(id=query.role_id).first()
            episode_data = YoutubeVids.objects.filter(id=query.episode_id).first()
            segment_data = MediaSegments.objects.filter(id=episode_data.segment_id).first()
            obj = {
                "episode_id": query.episode_id,
                "episode_title": episode_data.title,
                "episode_duration": episode_data.duration,
                "episode_date": episode_data.timestamp_aired,
                "media_segment_id": episode_data.media_segment_id,
                "media_segment_name": segment_data.name,
                "role": role_data.role,
            }
            episodes.append(obj)
        serialized = AirtimeSerializer(episodes, many=True)

        return Response(data={
            "total": {
                "appearances_count": len(episodes),
                "roles": list(set([x.get("role") for x in episodes])),
                # "segments": list(set([x.get("media_segment_name") for x in serialized]))
            },
            "episodes": serialized
        })

      
class FiltersAPIView(WAPIView):
    bundles = PeopleBundles.objects.all()
    serializer_class = BundleSerializer
    parser_classes = [JSONParser]

    def return_filters(self, request):
        bundles_options_raw = {bundle_type.value: [] for bundle_type in BundleType}
        for b in self.bundles:
            bundle_type_id = b.get("bundle_type_id")
            if bundle_type_id in BundleType.__members__:
                bundle_type = BundleType(bundle_type_id)
                bundles_options_raw[bundle_type.value].append(b)
        serialized_bundles = {x: BundleSerializer(y, many=True).data for x, y in bundles_options_raw.items()}

        age_options = [
            {"value": "all", "label": "all"},
            {"value": [None, 20], "label": "<20"},
            {"value": [20, 30], "label": "20-30"},
            {"value": [30, 50], "label": "30-50"},
            {"value": [50, 70], "label": "50-70"},
            {"value": [70, None], "label": "70+"},
        ]
        sex_options = [
            {"value": "all", "label": "all"},
            {"value": "m", "label": "male"},
            {"value": "f", "label": "female"}
        ]
        status_options = [
            {"value": "all", "label": "all"},
            {"value": "true", "label": "alive"},
            {"value": "false", "label": "dead"},
        ]
        return Response(data=[serialized_bundles, age_options, sex_options, status_options])


class PeopleExtendedAPIView(WAPIView):
    """
    API view to handle PeopleExtended data
    """
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
        logger.info(f"Received {len(request.data)} items")
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            logger.error(f'Invalid request data: {request.data}: {str(error)}')
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

        people = PeopleExtended.objects.all()
        logger.info(f'Before filtering: {len(people)}')

        # Apply filtering
        filter_value = request.data.get('filter', '')
        age_min = request.data.get('age_min', 1)
        age_max = request.data.get('age_max', 99)
        logger.info(f"Before: Age min is {age_min}, Age max is {age_max}")

        sex_filter = request.data.get('sex', None)

        # Tristate filters: True, False, None
        alive_filter = WAPIView.tristate_param(request.data.get('alive', None))
        # traitors_filter = WAPIView.tristate_param(request.data.get('is_ttu', None))
        # foreign_friends_filter = WAPIView.tristate_param(request.data.get('is_ff', None))

        if filter_value != '':
            people = people.filter(
                Q(fullname_en__icontains=filter_value) |
                Q(fullname_ru__icontains=filter_value) |
                Q(fullname_uk__icontains=filter_value)
            )
        if alive_filter is not None:
            people = people.filter(dod__isnull=alive_filter)
        if sex_filter is not None:
            people = people.filter(sex=sex_filter)

        today = datetime.now().date()
        if age_min and age_max:
            birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
            birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
            logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
            people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
        elif age_min and not age_max:
            birth_date_limit_min = today - timedelta(days=99 * 365)
            birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
            logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
            people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
        elif age_max and not age_min:
            birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
            birth_date_limit_max = today
            logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
            people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
        logger.info(f"After filtering: {len(people)}")

        # if traitors_filter is not None:
        #     people = people.filter(is_ttu=traitors_filter)
        #
        # if foreign_friends_filter is not None:
        #     people = people.filter(is_ff=foreign_friends_filter)

        # Apply sorting
        sort_by = request.data.get('sort_by', 'fullname.en')
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
        # people = PeopleExtended.objects.all()
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
                                       fields=['fullname'],
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


class TheoryAPIView(WAPIView):
    """
    API view to handle Theory table
    """
    queryset = Theory.objects.all()
    serializer_class = TheorySerializer
    parser_classes = [JSONParser]

    def __init__(self):
        """
        Initialize the class
        """
        super().__init__(request_handler={
            'general': self.return_general,
            'article': self.return_article
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

        # Filter articles by "publish_date" between "date_min" and "date_max"
        date_min_str = request.data.get('date_min', '01.01.1970')
        date_max_str = request.data.get('date_max', '31.12.2099')
        logger.info(f'Request date range [{date_min_str}; {date_max_str}]')

        try:
            date_min = datetime.strptime(date_min_str, '%d.%m.%Y')
            date_max = datetime.strptime(date_max_str, '%d.%m.%Y')
        except ValueError:
            logger.error(f'Invalid date format: {date_min_str} or {date_max_str}')
            return Response({'error': 'Invalid date format. Use DD.MM.YYYY format'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Use Q objects to filter articles by date range
        articles = articles.filter(Q(publish_date__gte=date_min) & Q(publish_date__lte=date_max))

        sort_by = request.data.get('sort_by', 'title')
        sort_direction = request.data.get('sort_direction', 'asc')
        sort_by = f'-{sort_by}' if sort_direction == 'desc' else sort_by
        logger.info(f'Sorting condition {sort_by}')
        articles = articles.order_by(sort_by)

        serializer = TheorySerializer(articles, many=True)
        return Response(data=serializer.data)

    @staticmethod
    def return_article(request):
        """
        Return single article
        """
        logger.info(f'Article request: {request.data}')
        article_id = request.data.get('id', None)
        if article_id is None:
            logger.error(f'Article id is not specified')
            return Response({'error': 'Article id is not specified'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            article = Theory.objects.get(id=article_id)
        except Theory.DoesNotExist:
            logger.error(f'Article id={article_id} does not exist')
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TheorySerializer(article)
        return Response(data=serializer.data)


def bad_request(request):
    """
    Return 400 Bad Request for GET requests
    """
    return HttpResponseBadRequest('<h1>400 Bad Request</h1>')
