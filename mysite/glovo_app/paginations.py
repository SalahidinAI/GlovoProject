from rest_framework.pagination import PageNumberPagination


class TwoObjectPagination(PageNumberPagination):
    page_size = 2
