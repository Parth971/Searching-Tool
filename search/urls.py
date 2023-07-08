from django.urls import path

from search.views import (
    FrameworkAPIVIew, FrameworkNamesAPIView, PreferencesAPIView,
    InquiryAPIView, FrameworkValuesAPIView, FrameworkDetailsAPIView,
    FilterFormDataAPIView, FrameworkNumberAPIView, SearchFormDataAPIView
)

urlpatterns = [
    # endpoints populate form
    path('framework-values/', FrameworkValuesAPIView.as_view(), name='search_framework_values'),
    path('filter-form-data/', FilterFormDataAPIView.as_view(), name='filter_form_data'),
    path('search-form-data/', SearchFormDataAPIView.as_view(), name='search_form_data'),

    # data apis
    path('framework/', FrameworkAPIVIew.as_view(), name='search_framework'),
    path('framework-detail/<int:framework_id>/', FrameworkDetailsAPIView.as_view(), name='framework_details'),
    path('framework-names/', FrameworkNamesAPIView.as_view(), name='framework_names'),
    path('framework-numbers/', FrameworkNumberAPIView.as_view(), name='framework_numbers'),
    path('preferences/', PreferencesAPIView.as_view(), name='preferences'),
    path('preferences/<int:framework_id>/', PreferencesAPIView.as_view(), name='delete_preferences'),
    path('inquiry/', InquiryAPIView.as_view(), name='inquiry'),
]
