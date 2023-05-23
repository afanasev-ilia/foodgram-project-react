import csv
import os

from django.core.management.base import BaseCommand

from foodgram import settings
from recipes.models import Ingredient


def ingredient_create(line):
    Ingredient.objects.get_or_create(
        name=line[0],
        measurement_unit=line[1],
    )


class Command(BaseCommand):
    help = 'Load ingredients to DB'

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'ingredients.csv')
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for line in reader:
                ingredient_create(line)
        self.stdout.write('successfull')
