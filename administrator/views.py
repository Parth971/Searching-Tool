from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from administrator.mixins import SearchVolumeDataMixin, SearchTopNamesMixin, SearchTopIndustriesMixin
from administrator.serializers import DurationSerializer, FrameworkDetailSerializer
from search.mixins import AdminFrameworkSearchQuery
from search.models import Framework
from search.permissions import IsSurveyFilled


class BaseSearchedDataAPIView(APIView):
    serializer_class = None
    duration = None

    def get_queryset(self):
        raise NotImplementedError('get_queryset() method is not implemented')

    def format_data(self, queryset):
        raise NotImplementedError('format_data() method is not implemented')

    def get_duration(self):
        assert self.duration is not None, f'duration must be set in {self.__class__.__name__} class'
        return self.duration

    def set_duration(self, duration):
        self.duration = duration

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.set_duration(serializer.data.get('duration'))

        queryset = self.get_queryset()
        data = self.format_data(queryset)

        return Response(status=status.HTTP_200_OK, data=data)


class SearchVolumeDataAPIView(SearchVolumeDataMixin, BaseSearchedDataAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DurationSerializer


class SearchTopNamesAPIView(SearchTopNamesMixin, BaseSearchedDataAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DurationSerializer


class SearchTopIndustriesAPIView(SearchTopIndustriesMixin, BaseSearchedDataAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DurationSerializer


class FrameworkSearchAPIView(AdminFrameworkSearchQuery, APIView):
    permission_classes = [IsAdminUser]
    results_per_page = 10

    def post(self, request, *args, **kwargs):
        self.is_data_valid(data=request.data, raise_error=True)
        framework_data = self.get_data()
        return Response(status=status.HTTP_200_OK, data=framework_data)


class FrameworkDetailAPIView(RetrieveAPIView):
    permission_classes = [IsSurveyFilled]
    serializer_class = FrameworkDetailSerializer
    queryset = Framework
    lookup_url_kwarg = 'framework_id'
