from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from supaword import settings


class CustomPostPagination(PageNumberPagination):
    """
    Custom pagination class with page size and page number from POST request
    E.g.:
    POST /api/people/ HTTP/1.1
    {
        "type": "all",
        "page": 1,
        "page_size": 20
    }
    """
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

    def get_page_number(self, request, paginator, view=None):
        """
        Get the page number from the request
        :param request: Object of type rest_framework.request.Request
        :param paginator: Object of type rest_framework.pagination.PageNumberPagination
        :param view: Object of type rest_framework.viewsets.ViewSet
        :return: Page number
        """
        page_number = request.data.get('page', 0)
        if page_number == 0:
            page_number = request.query_params.get('page', 0)
        if page_number == 0:
            page_number = 1
        return page_number

    def get_page_size(self, request):
        """
        Get the page size from the request
        """
        return request.data.get('page_size', request.query_params.get('page_size', self.page_size))

    def get_paginated_response(self, data):
        return Response(data={
            'total': self.page.paginator.count,
            'page_size': CustomPostPagination.page_size,
            'page': data
        }, headers={'Server-Version': settings.VERSION})
