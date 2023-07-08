import datetime
import json

from django.conf import settings
from django.core.management import BaseCommand

from survey.models import (
    InterestedCountry,
    Turnover,
    BusinessPercentage,
    PublicSectorBusinessTerritory,
    PublicSectorLanguage,
    PublicSectorCountry, Category, Sector, Industry
)


class Command(BaseCommand):
    help = 'Populate database'

    def add_arguments(self, parser):
        parser.add_argument(
            "--update",
            action="store_true",
            dest="update",
            help="updates data in db. if exists then skip else create new.",
        )

    def handle(self, *args, **options):
        update = options.get('update')
        if not update:
            print('Deleting existing data ...')
            models = (
                InterestedCountry,
                Turnover,
                BusinessPercentage,
                PublicSectorBusinessTerritory,
                PublicSectorLanguage,
                PublicSectorCountry
            )
            for model in models:
                model.objects.all().delete()

        with open(settings.BASE_DIR / 'survey/fixture/form_data.json', 'r') as f:
            data = json.load(f)

        self.process_data(data)
        print('Done')

    def process_data(self, data):
        countries = data.get('countries', [])
        turnovers = data.get('turnovers', [])
        business_percentages = data.get('business_percentages', [])
        public_sector_business_territories = data.get('public_sector_business_territories', [])
        public_sector_languages = data.get('public_sector_languages', [])
        public_sector_countries = data.get('public_sector_countries', [])
        categories = data.get('categories', [])
        industries = data.get('industries', [])
        sectors = data.get('sectors', [])

        maper = [
            (InterestedCountry, countries),
            (PublicSectorBusinessTerritory, public_sector_business_territories),
            (PublicSectorLanguage, public_sector_languages),
            (PublicSectorCountry, public_sector_countries),
            (Category, categories),
            (Industry, industries),
            (Sector, sectors),
        ]

        for model, data in maper:
            for value in data:
                self.create_object(model=model, data={'name': value})

        for turnover in turnovers:
            turnover = Turnover.extract_turnover(turnover)
            if turnover is None:
                raise ValueError(f"{turnover} is not a valid value format")

            minimum_value, maximum_value = turnover
            self.create_object(
                model=Turnover,
                data={'minimum_turnover': minimum_value, 'maximum_turnover': maximum_value}
            )

        for business_percentage in business_percentages:
            business_percentage = BusinessPercentage.extract_value(business_percentage)
            if business_percentage is None:
                raise ValueError(f"{business_percentage} is not a valid value format")

            self.create_object(
                model=BusinessPercentage,
                data={'value': business_percentage}
            )

    @staticmethod
    def create_object(model, data):
        model.objects.get_or_create(**data)
