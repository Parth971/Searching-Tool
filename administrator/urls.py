from django.urls import path

from administrator.views import (
    SearchVolumeDataAPIView, SearchTopIndustriesAPIView,
    FrameworkSearchAPIView, FrameworkDetailAPIView, SearchTopNamesAPIView
)

urlpatterns = [
    path('volume-data/', SearchVolumeDataAPIView.as_view(), name="clicked data"),
    path('top-searches/', SearchTopNamesAPIView.as_view(), name='search-top-3-names'),
    path('top-industries/', SearchTopIndustriesAPIView.as_view(), name='top_industries'),
    path('framework/search/', FrameworkSearchAPIView.as_view(), name='admin_framework_search'),
    path('framework/<int:framework_id>/', FrameworkDetailAPIView.as_view(), name='admin_framework_detail'),
]
