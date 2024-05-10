from datetime import timezone, datetime, timedelta
from functools import reduce
from enum import Enum
import arrow

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
from core.serializers import (PeopleExtendedBriefSerializer,
                              PeopleExtendedSerializer,
                              CacheSerializer,
                              BundleSerializer,
                              TheorySerializer,
                              AirtimeSerializer,
                              PopularStatsSerializer,
                              OrgsSerializer)
from core.requests import PagingRequestSerializer, TheoryRequestSerializer, OrgsRequestSerializer
from core.models import (PeopleExtended,
                         Theory,
                         PeopleBundles,
                         PeopleOnSmotrim,
                         PeopleOnYoutube,
                         MediaSegments,
                         YoutubeVids,
                         SmotrimEpisodes,
                         MediaRoles,
                         PopularStats,
                         OrgsExtended)
from core.pagination import CustomPostPagination

def bad_request(request):
    """
    Return 400 Bad Request for GET requests
    """
    return HttpResponseBadRequest('<h1>400 Bad Request</h1>')

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
        logger.info(f'INCOMING DATA ::: {request.data}')
        try:
            return self._post(request, *args, **kwargs)
        except Exception as e:
            logger.error(f'Exception in _post_protected WITH MESSAGE ::: {str(e)}')
            logger.error(f'Exception in _post_protected DATA ::: {request.data}')
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
            'timestamp': max_timestamp,
        }
        return Response(response_data)

    @staticmethod
    def apply_age_filter(age_min: int, age_max: int, dataset):
        today = arrow.now()
        ceiling = today.shift(days=-(int(age_min - 1) * 365)) if age_min else today
        floor = today.shift(days=-(int(age_max) * 365)) if age_max else today.shift(days=-(99 * 365))
        # if age_min and age_max:
        #     floor = today.shift(days=-(int(age_max) * 365))
        #     ceiling = today.shift(days=-(int(age_min - 1) * 365))
        #     # birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
        #     # birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
        #
        # elif age_min and not age_max:
        #     floor = today.shift(days=-(99 * 365))
        #     ceiling = today.shift(days=-(int(age_min - 1) * 365))
        #     # birth_date_limit_min = today - timedelta(days=99 * 365)
        #     # birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
        # elif age_max and not age_min:
        #     floor = today.shift(days=-(int(age_max) * 365))
        #     ceiling = today
        #     # birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
        #     # birth_date_limit_max = today
        # else: # neither params are sent over
        #     floor = today.shift(days=-(99 * 365))
        #     ceiling = today
        logger.info(f'Birth date limits: {floor.format()} - {ceiling.format()}')
        return dataset.filter(dob__gte=floor.format("YYYY-MM-DD"), dob__lte=ceiling.format("YYYY-MM-DD"))

    @staticmethod
    def apply_sex_filter(sex_filter: str, dataset):
        return people.filter(sex=sex_filter)

    @staticmethod
    def apply_alive_filter(alive_filter: bool, dataset):
        return dataset.filter(dod__isnull=alive_filter)

    @staticmethod
    def apply_custom_filter(custom_filter: str, dataset):
        return dataset.filter(
            Q(fullname_en__icontains=custom_filter) |
            Q(fullname_ru__icontains=custom_filter) |
            Q(fullname_uk__icontains=custom_filter)
        )

    @staticmethod
    def apply_bundle_filter(bundle_filter: list[int], dataset):
        filter_conditions = [Q(bundles__contains=[{"id": i}]) for i in bundle_filter]
        combined_filter = Q()  # Combine the Q objects using the OR operator '|'
        for condition in filter_conditions:
            combined_filter |= condition

        return dataset.filter(combined_filter)


    def apply_filters_to_dataset(self, request, dataset):
        # custom_filter = request.get("filter", "")
        # age_min, age_max = request.get("age_min", 1), request.get("age_max", 99)
        # sex_filter = request.get("sex", None)
        # alive_filter = self.tristate_param(request.data.get('alive', None))
        #
        # logger.debug(f"Before: Age min is {age_min}, Age max is {age_max}")

        dataset = self.apply_age_filter(request.get("age_min"), request.get("age_max"), dataset)

        if custom_filter := request.get("filter"):
            dataset = self.apply_custom_filter(custom_filter, dataset)
        if alive_filter := request.get("alive"):
            dataset = self.apply_alive_filter(alive_filter, dataset)
        if sex_filter := request.get("sex"):
            dataset = self.apply_sex_filter(sex_filter, dataset)
        if flags_filter := request.get("flags"):
            dataset = self.apply_bundle_filter(flags_filter, dataset)
        if expertise_filter := request.get("expertise"):
            dataset = self.apply_bundle_filter(expertise_filter, dataset)
        if groups_filter := request.get("groups"):
            dataset = self.apply_bundle_filter(groups_filter, dataset)

        # today = datetime.now().date()
        # if age_min and age_max:
        #     birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
        #     birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
        #     logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
        #     people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
        # elif age_min and not age_max:
        #     birth_date_limit_min = today - timedelta(days=99 * 365)
        #     birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
        #     logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
        #     people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
        # elif age_max and not age_min:
        #     birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
        #     birth_date_limit_max = today
        #     logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
        #     people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
        # logger.debug(f"After filtering: {len(people)}")

        return dataset

    def apply_sorting_to_dataset(self, request, dataset):
        sort_by = request.get("sort_by", "fullname.en")
        sort_direction = request.get("sort_direction", "asc")
        sort_by = f"-{sort_by}" if sort_direction == "desc" else sort_by
        logger.debug(f'Sorting condition {sort_by}')
        return dataset.order_by(sort_by)


    def return_page(self, request):
        """
        Return paginated and filtered data
        :param request: Object of type rest_framework.request.Request
        :return: Paginated and filtered data in short JSON format
        """
        req_serializer = PagingRequestSerializer(data=request.data)
        logger.info(f"Received {len(request.data)} items")
        try:
            req_serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            logger.error(f'Invalid request data: {request.data}: {str(error)}')
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

        people = PeopleExtended.objects.all()
        logger.debug(f'Before filtering: {len(people)}')
        people_filtered = self.apply_filters_to_dataset(req_serializer.validated_data, people)

        # Apply filtering
        # filter_value = request.data.get('filter', '')
        # age_min = request.data.get('age_min', 1)
        # age_max = request.data.get('age_max', 99)
        # logger.debug(f"Before: Age min is {age_min}, Age max is {age_max}")
        #
        # sex_filter = request.data.get('sex', None)
        #
        # # Tristate filters: True, False, None
        # alive_filter = WAPIView.tristate_param(request.data.get('alive', None))
        #
        # if filter_value != '':
        #     people = people.filter(
        #         Q(fullname_en__icontains=filter_value) |
        #         Q(fullname_ru__icontains=filter_value) |
        #         Q(fullname_uk__icontains=filter_value)
        #     )
        # if alive_filter is not None:
        #     people = people.filter(dod__isnull=alive_filter)
        # if sex_filter is not None:
        #     people = people.filter(sex=sex_filter)
        #
        # today = datetime.now().date()
        # if age_min and age_max:
        #     birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
        #     birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
        #     logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
        #     people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
        # elif age_min and not age_max:
        #     birth_date_limit_min = today - timedelta(days=99 * 365)
        #     birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
        #     logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
        #     people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
        # elif age_max and not age_min:
        #     birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
        #     birth_date_limit_max = today
        #     logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
        #     people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
        # logger.debug(f"After filtering: {len(people)}")

        # parse new filters

        # Apply sorting

        people_sorted = self.apply_sorting_to_dataset(req_serializer.validated_data, people_filtered)

        paginator = CustomPostPagination()
        result_page = paginator.paginate_queryset(people_sorted, request)
        serializer = PeopleExtendedSerializer(result_page, many=True)
        page = paginator.get_paginated_data(serializer.data)

        # Collect filters and popular stats
        filters = self.collect_filters()
        stats = self.collect_stats()

        response_data = {
            'page': page,
            'filters': filters,
            'stats': stats
        }

        return Response(response_data)

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

    # @staticmethod
    def return_person_data(self, request):
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

        airtime_data = self.unify_airtime_data(person_id)
        response_data = person_serializer.data

        # Combine the serialized data and return the response
        # response_data.update(airtime_data)
        # TODO: Serialize Organizations
        return Response({"person": response_data, "airtime": airtime_data})
        # return Response({"person": response_data})

    def unify_airtime_data(self, person_id):
        data = {"smotrim": self.collect_smotrim_airtime(person_id),
                "youtube": self.collect_youtube_airtime(person_id)}

        sorted_episodes = list()
        roles = set()
        unique_dates = set()
        total_airtime = 0

        for platform, episodes in data.items():
            if not episodes:
                continue
            for ep in episodes:
                if ep["role"]:
                    roles.add(ep["role"])
                total_airtime += ep.get("episode_duration", 0)
                k = arrow.get(ep["episode_date"])
                if k not in unique_dates:
                    unique_dates.add(k)
                    sorted_episodes.append({"date": k.format(), "episodes": [], "airtime": 0, "appearances": 0})

                for se in sorted_episodes:
                    if se["date"] == k.format():
                        serialized_ep = AirtimeSerializer(ep)
                        se["episodes"].append(serialized_ep.data)
                        se["airtime"] += ep.get("episode_duration", 0)
                        se["appearances"] += 1
        # logger.info(f"Collected {len(episodes)} episodes")

        return {
            "total": {"appearances_count": sum([se["appearances"] for se in sorted_episodes]),
                      "roles": list(roles),
                      "most_recent_appearance_date": max(unique_dates).format() if unique_dates else None,
                      "total_airtime": int(total_airtime) if total_airtime else 0},
            "episodes": sorted_episodes}


    @staticmethod
    def collect_smotrim_airtime(person_id):
        queryset = PeopleOnSmotrim.objects.filter(person_id=person_id)
        if not queryset:
            return []

        episodes = []
        for query in queryset:
            role_data = MediaRoles.objects.filter(id=query.media_role_id).first()
            episode_data = SmotrimEpisodes.objects.filter(id=query.episode_id).first()
            segment_data = MediaSegments.objects.filter(id=episode_data.segment_id).first()
            obj = {
                "episode_id": query.episode_id,
                "episode_title": episode_data.title,
                "episode_duration": episode_data.duration,
                "episode_date": episode_data.aired_on,
                "media_segment_id": episode_data.segment_id,
                "media_segment_name": segment_data.name if segment_data else None,
                "role": role_data.role if role_data else None,
                "source": "smotrim"
            }
            episodes.append(obj)

        return episodes

    @staticmethod
    def collect_youtube_airtime(person_id):
        queryset = PeopleOnYoutube.objects.filter(person_id=person_id)
        if not queryset:
            return []

        episodes = []
        for query in queryset:
            role_data = MediaRoles.objects.filter(id=query.media_role_id).first()
            episode_data = YoutubeVids.objects.filter(id=query.episode_id).first()
            segment_data = MediaSegments.objects.filter(id=episode_data.segment_id).first()
            obj = {
                "episode_id": query.episode_id,
                "episode_title": episode_data.title,
                "episode_duration": episode_data.duration,
                "episode_date": episode_data.aired_on,
                "media_segment_id": episode_data.segment_id,
                "media_segment_name": segment_data.name if segment_data else None,
                "role": role_data.role if role_data else None,
                "source": "youtube"
            }
            episodes.append(obj)

        return episodes

    def collect_filters(self):
        bundles = PeopleBundles.objects.all()
        logger.info(f"Have {len(bundles)} bundles in total")
        bundles_options_raw = {bundle_type.name: [] for bundle_type in BundleType}
        bundle_idx = [bundle_type.value for bundle_type in BundleType]
        for b in bundles:
            bundle_type_id = b.bundle_type_id
            if bundle_type_id in bundle_idx:
                bundle_type = BundleType(bundle_type_id).name
                bundles_options_raw[bundle_type].append(b)
        serialized_bundles = {x: BundleSerializer(y, many=True) for x, y in bundles_options_raw.items()}
        bundles_options = {x: y.data for x,y in serialized_bundles.items()}
        for k in bundles_options:
            bundles_options[k].append({"id": 0, "name": {"en": "all", "ru": "все", "uk": "всі"}})

        age_options = [
            {"value": [None, None], "label": "all"},
            {"value": [None, 20], "label": "<20"},
            {"value": [20, 30], "label": "20-30"},
            {"value": [30, 50], "label": "30-50"},
            {"value": [50, 70], "label": "50-70"},
            {"value": [70, None], "label": "70+"},
        ]
        sex_options = [
            {"value": None, "label": "all"},
            {"value": "m", "label": "male"},
            {"value": "f", "label": "female"}
        ]
        status_options = [
            {"value": None, "label": "all"},
            {"value": "true", "label": "alive"},
            {"value": "false", "label": "dead"},
        ]
        return {"bundles": bundles_options, "age": age_options, "gender": sex_options, "status": status_options}

    @staticmethod
    def collect_stats():
        data = PopularStats.objects.all()
        serialized = PopularStatsSerializer(data, many=True)
        return serialized.data


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


class OrgsAPIView(WAPIView):
    serializer_class = OrgsSerializer
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
            'person': self.return_org_data
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
        orgs = OrgsExtended.objects.filter(added_on__gt=created_after_datetime).order_by('id')
        serializer = CacheSerializer(orgs, many=True)

        # Find the maximum value of added_on across all people
        max_added_on_result = orgs.aggregate(max_added_on=Max('added_on'))
        max_added_on = max_added_on_result['max_added_on']
        max_timestamp = int(max_added_on.timestamp()) if max_added_on else created_after

        response_data = {
            'cache': serializer.data,
            'timestamp': max_timestamp,
        }
        return Response(response_data)

    # def apply_filters_to_dataset(self, request, dataset):
    #     # custom_filter = request.get("filter", "")
    #     # age_min, age_max = request.get("age_min", 1), request.get("age_max", 99)
    #     # sex_filter = request.get("sex", None)
    #     # alive_filter = self.tristate_param(request.data.get('alive', None))
    #     #
    #     # logger.debug(f"Before: Age min is {age_min}, Age max is {age_max}")
    #
    #     dataset = self.apply_age_filter(request.get("age_min"), request.get("age_max"), dataset)
    #
    #     if custom_filter := request.get("filter"):
    #         dataset = self.apply_custom_filter(custom_filter, dataset)
    #     if alive_filter := request.get("alive"):
    #         dataset = self.apply_alive_filter(alive_filter, dataset)
    #     if sex_filter := request.get("sex"):
    #         dataset = self.apply_sex_filter(sex_filter, dataset)
    #     if flags_filter := request.get("flags"):
    #         dataset = self.apply_bundle_filter(flags_filter, dataset)
    #     if expertise_filter := request.get("expertise"):
    #         dataset = self.apply_bundle_filter(expertise_filter, dataset)
    #     if groups_filter := request.get("groups"):
    #         dataset = self.apply_bundle_filter(groups_filter, dataset)
    #
    #     # today = datetime.now().date()
    #     # if age_min and age_max:
    #     #     birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
    #     #     birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
    #     #     logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
    #     #     people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
    #     # elif age_min and not age_max:
    #     #     birth_date_limit_min = today - timedelta(days=99 * 365)
    #     #     birth_date_limit_max = today - timedelta(days=int(age_min - 1) * 365)
    #     #     logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
    #     #     people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
    #     # elif age_max and not age_min:
    #     #     birth_date_limit_min = today - timedelta(days=int(age_max) * 365)
    #     #     birth_date_limit_max = today
    #     #     logger.info(f'Birth date limits: {birth_date_limit_min} - {birth_date_limit_max}')
    #     #     people = people.filter(dob__gte=birth_date_limit_min, dob__lte=birth_date_limit_max)
    #     # logger.debug(f"After filtering: {len(people)}")
    #
    #     return dataset

    # def apply_sorting_to_dataset(self, request, dataset):
    #     sort_by = request.get("sort_by", "fullname.en")
    #     sort_direction = request.get("sort_direction", "asc")
    #     sort_by = f"-{sort_by}" if sort_direction == "desc" else sort_by
    #     logger.debug(f'Sorting condition {sort_by}')
    #     return dataset.order_by(sort_by)

    def return_page(self, request):
        """
        Return paginated and filtered data
        :param request: Object of type rest_framework.request.Request
        :return: Paginated and filtered data in short JSON format
        """
        req_serializer = OrgsRequestSerializer(data=request.data)
        logger.info(f"Received {len(request.data)} items")
        try:
            req_serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            logger.error(f'Invalid request data: {request.data}: {str(error)}')
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

        orgs = OrgsExtended.objects.all()
        logger.debug(f'Before filtering: {len(orgs)}')

        # orgs_filtered = self.apply_filters_to_dataset(req_serializer.validated_data, orgs)
        # orgs_sorted = self.apply_sorting_to_dataset(req_serializer.validated_data, orgs_filtered)

        paginator = CustomPostPagination()
        result_page = paginator.paginate_queryset(orgs, request)
        serializer = OrgsSerializer(result_page, many=True)
        page = paginator.get_paginated_data(serializer.data)

        # Collect filters and popular stats
        filters = self.collect_filters()
        stats = self.collect_stats()

        response_data = {
            'page': page,
            'filters': filters,
            'stats': stats
        }

        return Response(response_data)

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
        orgs = OrgsExtended.objects.filter(reduce(lambda x, y: x | y, [
            Q(fullname_en=value) |
            Q(fullname_ru=value) |
            Q(fullname_uk=value) for value in values]))
        serializer = OrgsSerializer(orgs, many=True)
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
        orgs = search_model_fulltext(model=OrgsExtended,
                                     fields=['name', 'short_name'],
                                     values=values)

        serializer = OrgsSerializer(orgs, many=True)
        return Response(serializer.data)

    # @staticmethod
    def return_org_data(self, request):
        """
        Return person data
        :param request: Object of type rest_framework.request.Request
        :return: JSON response full data of the person
        """
        request_data = request.data
        org_id = request_data.get('id')

        try:
            org = OrgsExtended.objects.get(id=org_id)
        except OrgsExtended.DoesNotExist:
            logger.error(f'Person with id={org_id} does not exist')
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Serialize the person and organizations data
        logger.info(f'Person data request: {request_data}')
        org_serializer = OrgsSerializer(org)

        response_data = org_serializer.data

        return Response({"org": response_data})

    def collect_filters(self):
        pass
        # bundles = PeopleBundles.objects.all()
        # logger.info(f"Have {len(bundles)} bundles in total")
        # bundles_options_raw = {bundle_type.name: [] for bundle_type in BundleType}
        # bundle_idx = [bundle_type.value for bundle_type in BundleType]
        # for b in bundles:
        #     bundle_type_id = b.bundle_type_id
        #     if bundle_type_id in bundle_idx:
        #         bundle_type = BundleType(bundle_type_id).name
        #         bundles_options_raw[bundle_type].append(b)
        # serialized_bundles = {x: BundleSerializer(y, many=True) for x, y in bundles_options_raw.items()}
        # bundles_options = {x: y.data for x,y in serialized_bundles.items()}
        # for k in bundles_options:
        #     bundles_options[k].append({"id": 0, "name": {"en": "all", "ru": "все", "uk": "всі"}})
        #
        # age_options = [
        #     {"value": [None, None], "label": "all"},
        #     {"value": [None, 20], "label": "<20"},
        #     {"value": [20, 30], "label": "20-30"},
        #     {"value": [30, 50], "label": "30-50"},
        #     {"value": [50, 70], "label": "50-70"},
        #     {"value": [70, None], "label": "70+"},
        # ]
        # sex_options = [
        #     {"value": None, "label": "all"},
        #     {"value": "m", "label": "male"},
        #     {"value": "f", "label": "female"}
        # ]
        # status_options = [
        #     {"value": None, "label": "all"},
        #     {"value": "true", "label": "alive"},
        #     {"value": "false", "label": "dead"},
        # ]
        # return {"bundles": bundles_options, "age": age_options, "gender": sex_options, "status": status_options}

    @staticmethod
    def collect_stats():
        pass
        # data = PopularStats.objects.all()
        # serialized = PopularStatsSerializer(data, many=True)
        # return serialized.data
