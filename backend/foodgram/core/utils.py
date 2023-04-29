from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.utils import timezone


def paginate(
    request: HttpRequest,
    queryset: QuerySet,
    pagesize: int = settings.PAGE_SIZE,
) -> QuerySet:
    return Paginator(queryset, pagesize).get_page(request.GET.get('page'))


def truncatechars(chars: str, chars_limit: int = settings.NUMCATECHARS) -> str:
    return chars[:chars_limit] + '…' if len(chars) > chars_limit else chars


# def year_validator(value):
#     if value < 1900 or value > timezone.now().year:
#         raise ValidationError(
#             ('%(value)s is not a correcrt year!'),
#             params={'value': value},
#         )
