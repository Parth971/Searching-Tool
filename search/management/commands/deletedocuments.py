import elasticsearch
from django.conf import settings
from django.core.management import BaseCommand
from elasticsearch import Elasticsearch


class Command(BaseCommand):
    help = 'Delete documents from elasticsearch'
    index_name = settings.FRAMEWORK_INDEX_NAME

    def add_arguments(self, parser):
        parser.add_argument('ids', nargs='+', type=int, help='List of documents ids comma separated')

    def handle(self, *args, **options):
        ids = set(options.get('ids'))
        es = Elasticsearch(settings.ELASTIC_SEARCH_URL)

        for document_id in ids:
            try:
                es.delete(index=self.index_name, id=document_id)
                print(f'{document_id} is deleted successfully')
            except elasticsearch.exceptions.NotFoundError:
                print(f'{document_id} is not found')
