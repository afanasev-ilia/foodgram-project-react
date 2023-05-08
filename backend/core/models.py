from django.db import models


class DefaultModel(models.Model):
    class Meta:
        abstract = True
