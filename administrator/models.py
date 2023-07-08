from django.db import models

from accounts.models import User
from search.models import Framework


# Create your models here.

class SearchData(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    searched_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} searched "{self.framework.name}"'


class ViewData(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    searched_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} viewed "{self.framework.name}"'
