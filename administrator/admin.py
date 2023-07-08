from django.contrib import admin

from administrator.models import SearchData, ViewData

admin.site.register([SearchData, ViewData])
