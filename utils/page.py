"""Pagination utilities for DRF views."""
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    """
    Standard page-number pagination for GreaterWMS list endpoints.

    Configuration:
        - Default page size: 30 items
        - Configurable via `max_page` query parameter
        - Maximum page size: 1000 items
    """
    page_size: int = 30
    page_size_query_param: str = "max_page"
    max_page_size: int = 1000
    page_query_param: str = 'page'
