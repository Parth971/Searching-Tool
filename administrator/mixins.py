from datetime import datetime

from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils import timezone

from administrator.constants import MONTHLY, YEARLY
from administrator.models import SearchData
from search.models import Framework


class SearchVolumeDataMixin:
    date_formats = {
        MONTHLY: {
            'input_date_format': '%m',
            'output_date_format': '%B',
            'group_function': ExtractMonth,
            'output_key_name': 'month'
        },
        YEARLY: {
            'input_date_format': '%Y',
            'output_date_format': '%Y',
            'group_function': ExtractYear,
            'output_key_name': 'year'
        }
    }

    def format_data(self, queryset):
        duration = self.get_duration()
        duration_info = self.date_formats[duration]
        output_key_name = duration_info['output_key_name']
        input_date_format = duration_info['input_date_format']
        output_date_format = duration_info['output_date_format']

        return [
            {
                output_key_name: datetime.strptime(str(item['group']), input_date_format).strftime(output_date_format),
                'volume': item['volume']
            }
            for item in queryset
        ]

    def get_queryset(self):
        duration = self.get_duration()
        duration_info = self.date_formats[duration]
        group_function = duration_info['group_function']

        return SearchData.objects.annotate(
            group=group_function('searched_date')
        ).values('group').annotate(volume=Count('id'))


class SearchTopNamesMixin:

    def get_queryset(self):
        duration = self.get_duration()
        filters = {'searched_date__year': timezone.now().year}
        if duration == MONTHLY:
            filters['searched_date__month'] = timezone.now().month

        return SearchData.objects.filter(**filters).values('framework__name').annotate(
            number_of_searches=Count('id')
        ).order_by('-number_of_searches')[:3]

    def format_data(self, queryset):
        return [
            {
                'framework_name': item['framework__name'],
                'number_of_searches': item['number_of_searches']
            }
            for item in queryset
        ]


class SearchTopIndustriesMixin:

    def get_queryset(self):
        duration = self.get_duration()
        filters = {'searchdata__searched_date__year': timezone.now().year}
        if duration == MONTHLY:
            filters['searchdata__searched_date__month'] = timezone.now().month

        return Framework.objects.filter(
            searchdata__isnull=False, industry_or_category__isnull=False, **filters
        ).values('industry_or_category').annotate(
            number_of_searches=Count('searchdata')
        ).order_by('-number_of_searches')[:3]

    def format_data(self, queryset):
        return [
            {
                'industry': item['industry_or_category'],
                'number_of_searches': item['number_of_searches']
            }
            for item in queryset
        ]
