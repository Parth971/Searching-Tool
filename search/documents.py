from .models import Framework
from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl.registries import registry
from django.conf import settings

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@registry.register_document
class FrameworkDocument(Document):
    """Framework Elasticsearch document.

    name: To get similar words (html_strip analyser)
        raw: To search exact value
        suggest: To get suggestions

    number: To get similar words (html_strip analyser)
        raw: To search exact value
        search_as_you_type: To get suggestions as you type

    value: To get exact framework value
        Note: It should be used for range search so this value should be integer but as for now
        we use char field.

    industry_or_category: To get exact framework industry_or_category

    sub_category: To get exact framework sub_category

    start_date: To get exact framework start_date
        Note: date field is always used as range search

    end_date: To get exact framework end_date
        Note: date field is always used as range search

    cpvs:
        code: To get exact code related to framework

    """

    id = fields.IntegerField(attr='id')

    name = fields.TextField(
        fields={
            'raw': fields.KeywordField(),
            'search_as_you_type': fields.SearchAsYouTypeField(),
        },
        analyzer=html_strip
    )

    number = fields.TextField(
        fields={
            'raw': fields.KeywordField(),
            'search_as_you_type': fields.SearchAsYouTypeField(),
        },
        analyzer=html_strip
    )

    description = fields.KeywordField()
    value_number = fields.LongField()
    industry_or_category = fields.KeywordField()
    sub_category = fields.KeywordField()
    start_date = fields.DateField()
    end_date = fields.DateField()

    cpvs = fields.NestedField(
        properties={
            'code': fields.IntegerField(),
        }
    )

    class Index:
        name = settings.FRAMEWORK_INDEX_NAME
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1
        }

    class Django:
        model = Framework
