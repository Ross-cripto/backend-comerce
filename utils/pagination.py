"""
    This is a Custom Pagination .
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
        Class that defines custom pagination
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 32
    page_query_param = 'page'

    def get_paginated_response(self, data):
        """
            Defined the paginated response
        """
        return Response({
            'data': data,
            'meta': {
                'next': self.page.next_page_number()
                if self.page.has_next() else None,
                'previous': self.page.previous_page_number()
                if self.page.has_previous() else None,
                'count': self.page.paginator.count,
                }
        })
