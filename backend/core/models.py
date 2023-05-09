from behaviors.behaviors import Timestamped
from django.db import models


class DefaultModel(models.Model):
    class Meta:
        abstract = True


class TimestampedModel(DefaultModel, Timestamped):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('created').verbose_name = 'дата создания'
        self._meta.get_field('created').help_text = 'дата создания'
        self._meta.get_field('modified').verbose_name = 'дата изменения'
        self._meta.get_field('modified').help_text = 'дата изменения'

    class Meta:
        abstract = True
        ordering = ('-created',)
