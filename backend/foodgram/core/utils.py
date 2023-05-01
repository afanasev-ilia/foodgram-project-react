from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.utils import timezone


# class APIListPagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 10000


def truncatechars(chars: str, chars_limit: int = settings.NUMCATECHARS) -> str:
    return chars[:chars_limit] + '…' if len(chars) > chars_limit else chars


# def year_validator(value):
#     if value < 1900 or value > timezone.now().year:
#         raise ValidationError(
#             ('%(value)s is not a correcrt year!'),
#             params={'value': value},
#         )
