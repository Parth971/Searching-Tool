from rest_framework import status
from rest_framework.response import Response

from survey.constants import USER_SURVEY_COMPLETE, USER_SURVEY_INCOMPLETE
from survey.models import (
    InterestedCountry,
    Turnover,
    BusinessPercentage,
    PublicSectorLanguage,
    PublicSectorCountry,
    PublicSectorBusinessTerritory, Category, Sector, Industry
)


class CheckUserSurvey:
    success_message = USER_SURVEY_COMPLETE
    failed_message = USER_SURVEY_INCOMPLETE

    def check(self):
        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': self.success_message if self.request.user.is_survey_completed else self.failed_message,
                'code': int(self.request.user.is_survey_completed)
            }
        )


class QuerysetConverter:
    field_model_map = None

    def get_data(self):
        assert (
                self.field_model_map is not None
        ), f"'{self.__class__.__name__}' should include a `field_model_map` attribute, "

        return {
            field: list(map(str, model.objects.all()))
            for field, model in self.field_model_map.items()
        }


class SurveyFormData(QuerysetConverter):
    field_model_map = {
        'countries': InterestedCountry,
        'turnovers': Turnover,
        'business_percentages': BusinessPercentage,
        'public_sector_business_territories': PublicSectorBusinessTerritory,
        'public_sector_languages': PublicSectorLanguage,
        'public_sector_countries': PublicSectorCountry
    }

    def fetch(self):
        return self.get_data()


class SurveyCategories(QuerysetConverter):
    field_model_map = {
        'categories': Category,
    }

    def fetch(self):
        return self.get_data()


class SurveyIndustries(QuerysetConverter):
    field_model_map = {
        'industries': Industry,
    }

    def fetch(self):
        return self.get_data()


class SurveySectors(QuerysetConverter):
    field_model_map = {
        'sectors': Sector,
    }

    def fetch(self):
        return self.get_data()
