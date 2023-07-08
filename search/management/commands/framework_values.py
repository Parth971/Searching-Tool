import datetime
import json
import uuid

from django.conf import settings
from django.core.management import BaseCommand

from search.models import Framework, Cpv, Document, LOT, Supplier, FrameworkValue


class Command(BaseCommand):
    help = 'Populate framework value in database'

    def handle(self, *args, **options):
        print('Creating ...')
        with open(settings.BASE_DIR / 'search/fixture/framework_values.json', 'r') as f:
            data = json.load(f)
            FrameworkValue.objects.bulk_create([FrameworkValue(**block) for block in data])
            print('Done')
