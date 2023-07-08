from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Populate database'

    def handle(self, *args, **options):
        print('Creating active user ...')
        call_command('loaddata', 'accounts/fixture/active_user.json')
        print("Created")
