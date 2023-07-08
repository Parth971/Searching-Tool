from django.contrib import admin

from search.models import Framework, LOT, Supplier, Document, Cpv, FrameworkValue, Preference

admin.site.register([Framework, LOT, Supplier, Document, Cpv, FrameworkValue, Preference])
