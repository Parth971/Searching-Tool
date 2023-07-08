from django.contrib import admin

from survey.models import (
    InterestedCountry,
    PublicSectorCountry,
    PublicSectorLanguage,
    Industry,
    Sector,
    Survey,
    PublicSectorBusinessTerritory,
    BusinessPercentage,
    Category,
    Turnover
)

admin.site.register([
    InterestedCountry,
    PublicSectorCountry,
    PublicSectorLanguage,
    Industry,
    Sector,
    Survey,
    PublicSectorBusinessTerritory,
    BusinessPercentage,
    Category,
    Turnover
])
