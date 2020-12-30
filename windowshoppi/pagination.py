from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 60


class MediumResultsSetPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    max_page_size = 80


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardResultsSetLimitOffset(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100
