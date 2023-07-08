import contextlib
from django.conf import settings
from elasticsearch_dsl import Q
from django_elasticsearch_dsl import Document

from search.constants import DEFAULT_IMAGE_PATH, QUERY_TYPE_CHOICE_BY_NAME, QUERY_TYPE_CHOICE_BY_NUMBER, \
    QUERY_TYPE_CHOICE_BY_VALUE, QUERY_TYPE_CHOICE_SEARCH_ALL, DEFAULT_SUGGESTIONS_NUMBER
from search.documents import FrameworkDocument
from search.exceptions import EmptyQueryException
from search.models import FrameworkValue, Framework
from search.serializers import (
    FrameworkFullQuerySerializer, QueryByNameSerializer, QueryByNumberSerializer, AdminFrameworkQuerySerializer
)
from search.utils import get_model_object


class BaseSearchQuery:
    """
    Base class for building and executing search queries.

    Attributes:
        query_map (dict): A mapping of query names to corresponding query functions.
        document (type): The document type for the search query (subclass of django_elasticsearch_dsl.Document).
        serializers_to_try (list): A list of serializer classes and query names for input data validation.

    Instance Attributes:
        data: The validated data from the serializer.
        query_name: The name of the selected query.
        elasticsearch_response: The response obtained from executing the Elasticsearch query.
        query: The built query.
    """

    query_map = None
    document = None
    serializers_to_try = None

    def __init__(self):
        self.data = None
        self.query_name = None
        self.elasticsearch_response = None
        self.query = None

    def build_query(self):
        """
        Builds the search query based on the selected query name.

        Raises:
           ValueError: If the document is not a subclass of django_elasticsearch_dsl.Document.
           ValueError: If the query_name is not set or is None.
           ValueError: If the query function specified by query_name is not callable.

        Returns:
           dict: The built query.
        """
        if not issubclass(self.document, Document):
            raise ValueError(
                f'document must be of type django_elasticsearch_dsl.Document, '
                f'current document value is {self.document}'
            )

        if getattr(self, 'query_name') is None:
            raise ValueError(
                'is_data_valid() method must be called before calling build_query() method'
            )

        query_func = self.query_map[self.query_name]
        if callable(query_func):
            query = query_func()
        elif callable(getattr(self, query_func)):
            query = getattr(self, query_func)()
        else:
            raise ValueError(f'{query_func.__name__} is not callable')

        return query

    def execute_query(self):
        """
        Executes the built query using the Elasticsearch client.

        Returns:
            Response: The response obtained from executing the query.
        """
        return self.document.search().from_dict(self.query).execute()

    def get_result(self):
        """
        Retrieves the processed search results.

        Raises:
            NotImplementedError: If the subclass does not implement this method.

        Returns:
            Any: The processed search results.
        """
        raise NotImplementedError(
            f"Must implement get_result() method in  {self.__class__}"
        )

    def get_data(self):
        """
        Builds the query, executes it, and returns the processed search results.

        Returns:
            Any: The processed search results.
        """
        self.query = self.build_query()
        self.elasticsearch_response = self.execute_query()
        return self.get_result()

    def is_data_valid(self, data, raise_error=False):
        """
        Validates the input data using the provided serializers.

        Args:
            data: The input data to be validated.
            raise_error (bool): Whether to raise an error if no valid serializer is found (default: False).

        Returns:
            bool: True if a valid serializer is found, False otherwise.
        """
        serializers_to_try = self.serializers_to_try

        for serializer_class, query_name in serializers_to_try:
            serializer = serializer_class(data=data, context={'request': self.request})
            if serializer.is_valid(raise_exception=raise_error):
                self.query_name = query_name
                self.data = serializer.validated_data
                return True
        return False


class ListFrameworkNames(BaseSearchQuery):
    query_map = {
        'names': 'query_by_name'
    }
    serializers_to_try = [
        (QueryByNameSerializer, 'names')
    ]
    document = FrameworkDocument

    def query_by_name(self):
        framework_name = self.data.get('name')
        return {
            "query": {
                "multi_match": {
                    "query": framework_name,
                    "type": "bool_prefix",
                    "fields": [
                        "name.search_as_you_type"
                    ]
                }
            },
            "size": DEFAULT_SUGGESTIONS_NUMBER
        }

    def get_result(self):
        return [
            {
                'id': hit['_source']['id'],
                'name': hit['_source']['name'],
            }
            for hit in self.elasticsearch_response['hits']['hits']
        ]

    def build_query(self):
        return self.query_by_name()


class ListFrameworkNumber(BaseSearchQuery):
    query_map = {
        'number': 'query_by_number'
    }
    serializers_to_try = [
        (QueryByNumberSerializer, 'numbers')
    ]
    document = FrameworkDocument

    def query_by_number(self):
        """
        Builds a search query based on the framework number.

        Returns:
            dict: The built query.
        """
        framework_number = self.data.get('number')
        return {
            "query": {
                "multi_match": {
                    "query": framework_number,
                    "type": "bool_prefix",
                    "fields": [
                        "number.search_as_you_type"
                    ]
                }
            },
            "size": DEFAULT_SUGGESTIONS_NUMBER
        }

    def get_result(self):
        return [
            {
                'id': hit['_source']['id'],
                'number': hit['_source']['number'],
            }
            for hit in self.elasticsearch_response['hits']['hits']
        ]

    def build_query(self):
        return self.query_by_number()


class FrameworkSearchQuery(BaseSearchQuery):
    query_map = {
        'full': 'full_query'
    }
    serializers_to_try = [
        (FrameworkFullQuerySerializer, 'full')
    ]
    document = FrameworkDocument
    results_per_page = None

    def __init__(self):
        super().__init__()
        self.filters = None
        self.page = 1

    def build_query(self):
        """
        Builds the search query based on the specified filters, page, and results_per_page.

        Returns:
            dict: The built query.
        """
        page_param = self.request.data.get('page', '')

        if isinstance(page_param, int) or (
                isinstance(page_param, str) and page_param.isdigit() and int(page_param) > 0):
            self.page = int(page_param)

        results_per_page_param = self.request.data.get('results_per_page', '')

        if isinstance(results_per_page_param, int) \
                or (
                isinstance(results_per_page_param, str)
                and results_per_page_param.isdigit()
                and int(results_per_page_param) > 0
        ):
            self.results_per_page = int(results_per_page_param)

        if self.results_per_page is None:
            raise ValueError(
                'results_per_page must be set'
            )

        from_value = (self.page - 1) * self.results_per_page
        bool_query = super(FrameworkSearchQuery, self).build_query()

        query = {
            'query': bool_query,
            'from': from_value,
            'size': self.results_per_page
        }

        if self.filters:
            query['post_filter'] = {
                'bool': {
                    'should': self.filters
                }
            }

        return query

    def get_data(self):
        """
        Retrieves the processed search results along with pagination information.

        Returns:
            dict: Dictionary containing total_count, page, results_per_page, and data.
        """
        data = []
        with contextlib.suppress(EmptyQueryException):
            data = super().get_data()

        return {
            'total_count': self.elasticsearch_response['hits']['total']['value'] if self.elasticsearch_response else 0,
            'page': self.page,
            'results_per_page': self.results_per_page,
            'data': data
        }

    def set_filter_query(self, filters):
        """
        Sets the filter queries based on the provided filters.

        Args:
            filters (dict): Dictionary containing filter values.
        """
        filter_queries = []

        if filters.get('cpv_code'):
            filter_queries.append(Q('nested', path='cpvs', query=Q('match', **{'cpvs.code': filters.get('cpv_code')})))

        if filters.get('industry_category_type'):
            filter_queries.append(Q('term', industry_or_category=filters.get('industry_category_type')))

        if filters.get('sub_category'):
            filter_queries.append(Q('term', sub_category=filters.get('sub_category')))

        if filters.get('start_date'):
            filter_queries.append(
                Q('range', start_date={'gte': filters.get('start_date'), 'lte': filters.get('start_date')}))

        if filters.get('end_date'):
            filter_queries.append(Q('range', end_date={'gte': filters.get('end_date'), 'lte': filters.get('end_date')}))

        if filter_queries:
            self.filters = filter_queries

    def get_must_queries(self, query_type, query):
        """
        Gets the must queries based on the query type and query value.

        Args:
            query_type (str): The type of query.
            query (dict): The query values.

        Returns:
            list: List of must queries.
        """
        must_queries = []

        if query_type == QUERY_TYPE_CHOICE_BY_NAME and query.get('value'):
            must_queries.append(Q('match_phrase', name=query['value']))
        elif query_type == QUERY_TYPE_CHOICE_BY_NUMBER and query.get('value'):
            must_queries.append(Q('match_phrase', number=query['value']))
        elif query_type == QUERY_TYPE_CHOICE_BY_VALUE and query.get('value'):
            framework_value_object = get_model_object(model_class=FrameworkValue, query={'value': query['value']})

            value_number = {}
            if framework_value_object.minimum_value:
                value_number['gte'] = framework_value_object.minimum_value

            if framework_value_object.maximum_value:
                value_number['lte'] = framework_value_object.maximum_value

            must_queries.append(Q('range', value_number=value_number))
        elif query_type == QUERY_TYPE_CHOICE_SEARCH_ALL:
            if query.get('value'):
                number_fields = []
                if query['value'].isdigit():
                    must_queries.append(
                        Q(
                            'match',
                            value_number=int(query['value'])
                        )
                    )
                    number_fields = ["cpvs.code", "value_number"]
                must_queries.append(
                    Q(
                        'multi_match',
                        query=query['value'],
                        fields=["name", "description", "number.raw", *number_fields]
                    )
                )

            if query.get('preference_frameworks'):
                preference_frameworks_ids = Framework.objects.get_user_preferences(
                    user=self.request.user, preference_names=query.get('preference_frameworks')
                ).values_list('id', flat=True)
                must_queries.append(Q('terms', **{"id": list(preference_frameworks_ids)}))

        return must_queries

    def full_query(self):
        """
        Builds the full search query based on the specified query type and filters.

        Returns:
            dict: The built query.
        """
        query_type = self.data.get('query_type')

        query = self.data.get('query')
        filters = self.data.get('filter')

        self.set_filter_query(filters)

        result_query = {}
        if must_queries := self.get_must_queries(query_type, query):
            result_query['bool'] = {'should': must_queries}
        else:
            raise EmptyQueryException

        return result_query

    def get_result(self):
        """
        Processes the search results and returns a list of framework information.

        Returns:
            list: List of dictionaries containing framework information.
        """
        results = []
        if self.elasticsearch_response is not None:
            for hit in self.elasticsearch_response['hits']['hits']:
                framework = get_model_object(model_class=Framework, query={'id': hit['_source']['id']})
                if not framework:
                    continue

                image_url = DEFAULT_IMAGE_PATH % settings.BACK_END_DOMAIN
                if framework.logo:
                    image_url = settings.BACK_END_DOMAIN + settings.MEDIA_URL + framework.logo
                results.append(
                    {
                        'framework_id': hit['_source']['id'],
                        'framework_name': hit['_source']['name'],
                        'framework_number': hit['_source']['number'],
                        'framework_value': framework.value,
                        'industry_type': hit['_source']['industry_or_category'],
                        'sub_category': hit['_source']['sub_category'],
                        'description': hit['_source']['description'],
                        'start_date': hit['_source']['start_date'],
                        'end_date': hit['_source']['end_date'],
                        'framework_image': image_url
                    }
                )
        return results


class AdminFrameworkSearchQuery(BaseSearchQuery):
    query_map = {
        'full': 'full_query'
    }
    serializers_to_try = [
        (AdminFrameworkQuerySerializer, 'full')
    ]
    document = FrameworkDocument
    results_per_page = None

    def __init__(self):
        super().__init__()
        self.page = 1

    def build_query(self):
        """
        Builds the search query based on the request data.

        Returns:
            dict: The built search query.

        Raises:
            ValueError: If results_per_page is not set.
        """
        page_param = self.request.data.get('page', '')

        if isinstance(page_param, int) or (
                isinstance(page_param, str) and page_param.isdigit() and int(page_param) > 0):
            self.page = int(page_param)

        results_per_page_param = self.request.data.get('results_per_page', '')

        if isinstance(results_per_page_param, int) \
                or (
                isinstance(results_per_page_param, str)
                and results_per_page_param.isdigit()
                and int(results_per_page_param) > 0
        ):
            self.results_per_page = int(results_per_page_param)

        if self.results_per_page is None:
            raise ValueError(
                'results_per_page must be set'
            )

        from_value = (self.page - 1) * self.results_per_page
        bool_query = super(AdminFrameworkSearchQuery, self).build_query()

        return {
            'query': bool_query,
            'from': from_value,
            'size': self.results_per_page,
        }

    def get_data(self):
        """
        Retrieves the search data, including total count, page information, and search results.

        Returns:
            dict: The search data.
        """
        data = []
        with contextlib.suppress(EmptyQueryException):
            data = super().get_data()

        return {
            'total_count': self.elasticsearch_response['hits']['total']['value'] if self.elasticsearch_response else 0,
            'page': self.page,
            'results_per_page': self.results_per_page,
            'data': data
        }

    def get_must_queries(self):
        """
        Retrieves the must queries based on the request data.

        Returns:
            list: List of must queries.
        """
        frameworks = self.data.get('frameworks')
        industry_category_types = self.data.get('industry_category_types')
        sub_categories = self.data.get('sub_categories')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')

        must_queries = []

        if frameworks:
            must_queries.append(Q('terms', **{"name.raw": frameworks}))

        if industry_category_types:
            must_queries.append(Q('terms', **{"industry_or_category": industry_category_types}))

        if sub_categories:
            must_queries.append(Q('terms', **{"sub_category": sub_categories}))

        if start_date and end_date:
            must_queries.extend([
                Q('range', start_date={'gte': start_date, 'lte': start_date}),
                Q('range', end_date={'gte': end_date, 'lte': end_date})
            ])

        return must_queries

    def full_query(self):
        """
        Builds the full search query based on the must queries.

        Returns:
            dict: The full search query.
        """
        result_query = {}
        if must_queries := self.get_must_queries():
            result_query['bool'] = {'must': must_queries}
        else:
            result_query['match_all'] = {}

        return result_query

    def get_result(self):
        """
        Processes the search results and returns a list of framework information.

        Returns:
            list: List of dictionaries containing framework information.
        """
        results = []
        if self.elasticsearch_response is not None:
            for hit in self.elasticsearch_response['hits']['hits']:
                framework = get_model_object(model_class=Framework, query={'id': hit['_source']['id']})
                image_url = DEFAULT_IMAGE_PATH % settings.BACK_END_DOMAIN
                if framework.logo:
                    image_url = settings.BACK_END_DOMAIN + settings.MEDIA_URL + framework.logo
                results.append(
                    {
                        'framework_id': hit['_source']['id'],
                        'framework_name': hit['_source']['name'],
                        'number': hit['_source']['number'],
                        'start_date': hit['_source']['start_date'],
                        'framework_image': image_url
                    }
                )
        return results
