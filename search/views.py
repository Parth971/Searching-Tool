from django.db.models import F, Q
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from administrator.models import ViewData
from search.constants import (
    DEFAULT_RESULTS_PER_PAGE, INQUIRY_EMAIL_SENT,
    PREFERENCE_DELETED, PREFERENCE_CREATED,
    INVALID_FRAMEWORK_SEARCH
)
from search.mixins import FrameworkSearchQuery, ListFrameworkNames, ListFrameworkNumber
from search.models import FrameworkValue, Framework, Preference
from search.permissions import IsSurveyFilled, IsPreferenceOwner
from search.serializers import (
    FrameworkDetailSerializer, PreferencesSerializer,
    InquirySerializer, IndustryTypeSerializers
)
from search.utils import send_inquiry_email, search_data


class FrameworkAPIVIew(FrameworkSearchQuery, APIView):
    """
    Based on the query or filter, it will return the list of frameworks
    """
    permission_classes = [IsAuthenticated, IsSurveyFilled]
    results_per_page = DEFAULT_RESULTS_PER_PAGE

    def post(self, request, *args, **kwargs):
        if self.is_data_valid(data=request.data):
            framework_data = self.get_data()
            search_data(framework_data['data'], request.user)
            return Response(status=status.HTTP_200_OK, data=framework_data)
        return Response(data={'message': INVALID_FRAMEWORK_SEARCH}, status=status.HTTP_400_BAD_REQUEST)


class FrameworkValuesAPIView(APIView):
    """
    This API is used for Populating "Search with value" form
    """
    permission_classes = [IsAuthenticated, IsSurveyFilled]
    model = FrameworkValue

    def get(self, request):
        data = {"framework_values": self.model.get_values()}
        return Response(status=status.HTTP_200_OK, data=data)


class FrameworkNamesAPIView(ListFrameworkNames, APIView):
    """
    Based on framework name, it will return suggested list of framework names from elasticsearch query
    """
    permission_classes = [IsAuthenticated, IsSurveyFilled]

    def post(self, request):
        data = {'name': request.data.get('framework_name')}
        if self.is_data_valid(data=data):
            return Response(status=status.HTTP_200_OK, data=self.get_data())
        return Response(data={'message': INVALID_FRAMEWORK_SEARCH}, status=status.HTTP_400_BAD_REQUEST)


class FrameworkNumberAPIView(ListFrameworkNumber, APIView):
    """
    Based on framework number, it will return suggested list of framework number from elasticsearch query
    """
    permission_classes = [IsAuthenticated, IsSurveyFilled]

    def post(self, request):
        data = {'number': request.data.get('framework_number')}
        if self.is_data_valid(data=data):
            return Response(status=status.HTTP_200_OK, data=self.get_data())
        return Response(data={'message': INVALID_FRAMEWORK_SEARCH}, status=status.HTTP_400_BAD_REQUEST)


class FrameworkDetailsAPIView(RetrieveAPIView):
    """
    API view for retrieving framework details based on the framework ID.

    Permissions:
        - User must be authenticated.
        - User must have filled out the survey.

    Attributes:
        permission_classes (list): List of permission classes.
        serializer_class (FrameworkDetailSerializer): The serializer class for framework details.
        queryset (QuerySet): The queryset for retrieving framework objects.
        lookup_url_kwarg (str): The URL keyword argument for specifying the framework ID.

    Methods:
        get(request, *args, **kwargs): Retrieve and return the framework details.
    """

    permission_classes = [IsAuthenticated, IsSurveyFilled]
    serializer_class = FrameworkDetailSerializer
    queryset = Framework.objects
    lookup_url_kwarg = 'framework_id'

    def get(self, request, *args, **kwargs):
        framework = self.get_object()
        ViewData.objects.create(framework=framework, user=user)
        return super().get(request, *args, **kwargs)


class PreferencesAPIView(DestroyAPIView, ListCreateAPIView):
    """
    API view for managing preferences.

    Permissions:
        - User must be authenticated.
        - User must have filled out the survey.
        - User must be the owner of the preference.

    Attributes:
        permission_classes (list): List of permission classes.
        serializer_class (PreferencesSerializer): Serializer class for preferences.
        lookup_url_kwarg (str): Name of the URL keyword argument for framework ID.
        queryset (QuerySet): QuerySet for preferences.
        pagination_class (None): Disable pagination.

    Methods:
        get_queryset(): Get the queryset for preferences.
        list(request, *args, **kwargs): List preferences for the current user.
        create(request, *args, **kwargs): Create a new preference for the current user.
        destroy(request, *args, **kwargs): Delete a preference for the current user.
    """
    permission_classes = [IsAuthenticated, IsSurveyFilled, IsPreferenceOwner]
    serializer_class = PreferencesSerializer
    lookup_url_kwarg = 'framework_id'
    queryset = Preference.objects.all()
    pagination_class = None

    def get_queryset(self):
        """
        Get the queryset for preferences filtered by the current user.

        Returns:
            QuerySet: Filtered queryset for preferences.
        """
        return self.queryset.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Get the queryset for preferences filtered by the current user.

        Returns:
            QuerySet: Filtered queryset for preferences.
        """
        data = self.get_queryset().values('id', name=F('framework__name'))
        return Response(data)

    def create(self, request, *args, **kwargs):
        """
        Create a new preference for the current user.

        Args:
            request (Request): The incoming request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: Response with the created preference.
        """
        serializer = self.get_serializer(data={**request.data, 'user': request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            **serializer.data,
            'message': PREFERENCE_CREATED
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a preference for the current user.

        Args:
            request (Request): The incoming request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: Response with the success message.
        """
        response = super().destroy(request, *args, **kwargs)
        response.data = {
            'message': PREFERENCE_DELETED
        }
        response.status_code = status.HTTP_200_OK
        return response


class InquiryAPIView(APIView):
    """
    API view for sending inquiry emails.

    Permissions:
        - User must be authenticated.
        - User must have filled out the survey.

    Attributes:
        permission_classes (list): List of permission classes.
        serializer_class (InquirySerializer): Serializer class for inquiry data.

    Methods:
        post(request, *args, **kwargs): Send an inquiry email.
    """
    permission_classes = [IsAuthenticated, IsSurveyFilled]
    serializer_class = InquirySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        context = serializer.get_email_context()
        send_inquiry_email(request.user, **context)
        return Response(status=status.HTTP_200_OK, data={"message": INQUIRY_EMAIL_SENT})


class FilterFormDataAPIView(APIView):
    """
    API view for retrieving industry and sub-category data for populating the filter form in the result page.

    Permissions:
        - User must be authenticated.
        - User must have filled out the survey.

    Attributes:
        permission_classes (list): List of permission classes.
        model (Framework): The model class for retrieving data.

    Methods:
        get(request): Retrieve industry and sub-category data.
    """

    permission_classes = [IsAuthenticated, IsSurveyFilled]
    model = Framework

    def get(self, request):
        industry_types = self.model.objects.values_list('industry_or_category', flat=True).distinct()
        sub_categories = self.model.objects.values_list('sub_category', flat=True).distinct()

        data = {
            'industry_types': list(filter(lambda item: item is not None, industry_types)),
            'sub_categories': list(filter(lambda item: item is not None, sub_categories)),
        }
        return Response(status=status.HTTP_200_OK, data=data)


class SearchFormDataAPIView(APIView):
    """
    API view for retrieving industry and sub-category data for populating the filter form in the admin's search page.

    Requests options:
    - If empty body is provided then response will contain list of all industries
    - If body contains list of industries then response will contain list of given industries and all related sub-categories

    Permissions:
        - User must be authenticated.
        - User must have filled out the survey.

    Attributes:
        permission_classes (list): List of permission classes.
        model (Framework): The model class for retrieving data.
        serializer (IndustryTypeSerializers): The serializer class for validating request data.

    Methods:
        post(request): Retrieve industry and sub-category data based on request options.
    """

    permission_classes = [IsAuthenticated, IsSurveyFilled]
    model = Framework
    serializer = IndustryTypeSerializers

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = {}
        sub_categories_query = self.model.objects.all()

        if industry_types := serializer.data.get('industry_types'):
            data['industry_types'] = industry_types
            sub_categories_query = sub_categories_query.filter(industry_or_category__in=industry_types)
            data['sub_categories'] = sub_categories_query.values_list('sub_category', flat=True).distinct()
        else:
            data['industry_types'] = self.model.objects.exclude(
                Q(industry_or_category=None) | Q(industry_or_category__exact="")
            ).values_list('industry_or_category', flat=True).distinct()

        return Response(status=status.HTTP_200_OK, data=data)
