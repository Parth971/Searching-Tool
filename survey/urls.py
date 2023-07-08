from django.urls import path

from survey.views import (
    CheckUserSurveyData,
    UserSurveyData,
    SurveyFormDataAPIView,
    SurveyCategoriesAPIView,
    SurveySectorsAPIView,
    SurveyIndustriesAPIView
)

urlpatterns = [
    path('check-user-survey/', CheckUserSurveyData.as_view(), name='check_user_survey'),
    path('user-survey/', UserSurveyData.as_view(), name='save_user_survey'),
    path('form-data/', SurveyFormDataAPIView.as_view(), name='survey_form_data'),
    path('categories/', SurveyCategoriesAPIView.as_view(), name='survey_categories'),
    path('industries/', SurveyIndustriesAPIView.as_view(), name='survey_industries'),
    path('sectors/', SurveySectorsAPIView.as_view(), name='survey_sectors'),

]
