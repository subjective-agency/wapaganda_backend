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
    min_page_size = 10
    max_page_size = 100
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

    def get_page_number(self, request, paginator, view=None):
        """
        Get the validated page number from the request
        :param request: Object of type rest_framework.request.Request
        :param paginator: Object of type rest_framework.pagination.PageNumberPagination
        :param view: Object of type rest_framework.viewsets.ViewSet
        :return: Page number
        """
        page_number = request.data.get('page', 0)
        if not isinstance(page_number, int):
            raise ValueError(f"Invalid page_number {page_number} type; must be an integer")
        if page_number == 0:
            page_number = request.query_params.get('page', 0)
        if page_number == 0:
            page_number = 1
        return page_number

    def get_page_size(self, request):
        """
        Get the validated page size from the request
        """
        page_size = request.data.get('page_size', request.query_params.get('page_size', self.page_size))
        if not isinstance(page_size, int):
            raise ValueError(f"Invalid page_size {page_size} type; must be an integer")
        if page_size < 1:
            raise ValueError(f"Invalid page_size {page_size} size; must be a positive integer")
        elif page_size < self.min_page_size:
            page_size = self.min_page_size
        elif page_size > self.max_page_size:
            page_size = self.max_page_size
        return page_size

    def get_paginated_response(self, data):
        """
        Return the paginated response, add total number of records and page size
        Add server version to the response headers
        :return: Object of type rest_framework.response.Response
        """
        return Response(data={
            'total': self.page.paginator.count,
            'page_size': CustomPostPagination.page_size,
            'page': data
        })
