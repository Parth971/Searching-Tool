from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from survey.mixins import (
    CheckUserSurvey,
    SurveyFormData,
    SurveyCategories,
    SurveyIndustries,
    SurveySectors
)
from survey.serializers import CreateUpdateUserSurveyDataSerializer


class CheckUserSurveyData(CheckUserSurvey, APIView):
    def get(self, request, *args, **kwargs):
        return self.check()


class UserSurveyData(RetrieveModelMixin, GenericAPIView):
    serializer_class = CreateUpdateUserSurveyDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create({**serializer.validated_data, 'user': self.request.user})
        return Response(status=status.HTTP_200_OK, data={
            "message": "Survey data saved",
        })

    def get(self, request, *args, **kwargs):
        if self.request.user.is_survey_completed:
            return self.retrieve(request, *args, **kwargs)
        return Response(data={'message': "Survey is not filed"}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        return self.request.user.survey


class SurveyFormDataAPIView(SurveyFormData, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK, data=self.fetch())


class SurveyCategoriesAPIView(SurveyCategories, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK, data=self.fetch())


class SurveyIndustriesAPIView(SurveyIndustries, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK, data=self.fetch())


class SurveySectorsAPIView(SurveySectors, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK, data=self.fetch())
