import re

from django.db import models

from accounts.models import User


class InterestedCountry(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Interested countries"

    def __str__(self):
        return self.name


class Turnover(models.Model):
    minimum_turnover = models.IntegerField()
    maximum_turnover = models.IntegerField(null=True)

    def __str__(self):
        if self.maximum_turnover is None:
            return f"{self.minimum_turnover} Million plus"
        return f"{self.minimum_turnover} - {self.maximum_turnover} Million"

    @classmethod
    def extract_turnover(cls, display_value):
        pattern = r"^(\d{1,2})\s*-\s*(\d{1,2})\s*Million$"
        match = re.search(pattern, display_value)
        if match:
            minimum_value = int(match[1])
            maximum_value = int(match[2])
            return minimum_value, maximum_value

        pattern = r"^(\d{1,2})\s*Million plus$"
        match = re.search(pattern, display_value)
        if match:
            minimum_value = int(match[1])
            return minimum_value, None


class BusinessPercentage(models.Model):
    value = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.value}%"

    @classmethod
    def extract_value(cls, display_value):
        pattern = r"(\d+)%"
        match = re.search(pattern, display_value)
        if match:
            return int(match[1])


class PublicSectorLanguage(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PublicSectorCountry(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Public sector countries"

    def __str__(self):
        return self.name


class PublicSectorBusinessTerritory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Public sector business territories"

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Survey(models.Model):
    user = models.OneToOneField(User, related_name='survey', on_delete=models.CASCADE)
    country = models.ForeignKey(InterestedCountry, related_name='surveys', on_delete=models.SET_NULL, null=True)
    turnover = models.ForeignKey(Turnover, related_name='surveys', on_delete=models.SET_NULL, null=True)
    business_percentage = models.ForeignKey(BusinessPercentage, related_name='surveys', on_delete=models.SET_NULL,
                                            null=True)

    public_sector_languages = models.ManyToManyField(
        PublicSectorLanguage, related_name='surveys'
    )
    public_sector_countries = models.ManyToManyField(
        PublicSectorCountry, related_name='surveys'
    )
    public_sector_business_territories = models.ManyToManyField(
        PublicSectorBusinessTerritory, related_name='surveys'
    )

    industry = models.ForeignKey(Industry, related_name='surveys', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, related_name='surveys', on_delete=models.CASCADE, null=True)
    sector = models.ForeignKey(Sector, related_name='surveys', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.email
