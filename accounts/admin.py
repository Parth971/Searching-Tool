from django.contrib import admin

from accounts.models import User, ActivateUserToken

admin.site.register([User, ActivateUserToken])
