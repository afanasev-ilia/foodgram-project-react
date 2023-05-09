from django.conf import settings
from rest_framework.pagination import PageNumberPagination

# from django.db.models import QuerySet
# from django.http import HttpRequest
# from django.core.exceptions import ValidationError
# from django.utils import timezone


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'


def truncatechars(chars: str, chars_limit: int = settings.NUMCATECHARS) -> str:
    return chars[:chars_limit] + '…' if len(chars) > chars_limit else chars
