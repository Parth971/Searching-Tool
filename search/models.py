import datetime

from django.db import models

from accounts.models import User
from search.managers import FrameworkModelManager


class Framework(models.Model):
    """
    Model representing a framework.

    Fields:
        name (TextField): The name of the framework.
        link (TextField, optional): The link associated with the framework. Defaults to None.
        site_name (CharField): The name of the site associated with the framework.
        number (CharField, optional): The number of the framework. Defaults to None.
        lot_number (IntegerField, optional): The lot number associated with the framework. Defaults to None.
        value (CharField, optional): The value of the framework. Defaults to None.
        value_number (BigIntegerField, optional): The numeric value of the framework. Defaults to None.
        start_date (DateField, optional): The start date of the framework. Defaults to None.
        end_date (DateField, optional): The end date of the framework. Defaults to None.
        service_type (TextField, optional): The type of service provided by the framework. Defaults to None.
        description (TextField, optional): The description of the framework. Defaults to None.
        logo (TextField, optional): The URL or path of the framework's logo. Defaults to None.
        industry_or_category (CharField, optional): The industry or category associated with the framework. Defaults to None.
        sub_category (CharField, optional): The sub-category associated with the framework. Defaults to None.
        is_available (BooleanField): Indicates if the framework is available. Defaults to True.
        created_at (DateField): The date when the framework was created.
        updated_at (DateField): The date when the framework was last updated.

    Related Fields:
        cpvs (related_name='cpvs', ForeignKey): The CPV codes associated with the framework.
        documents (related_name='documents', ForeignKey): The documents associated with the framework.
        lots (related_name='lots', ForeignKey): The lots associated with the framework.
        suppliers (related_name='suppliers', ForeignKey): The suppliers associated with the framework.
        preferences (related_name='preferences', ForeignKey): The user preferences for the framework.

    Methods:
        save(*args, **kwargs): Overrides the save method to update the 'updated_at' field.
    """

    name = models.TextField()
    link = models.TextField(null=True)
    site_name = models.CharField(max_length=255)
    number = models.CharField(null=True, max_length=200)
    lot_number = models.IntegerField(null=True)
    value = models.CharField(max_length=255, null=True)
    value_number = models.BigIntegerField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    service_type = models.TextField(null=True)
    description = models.TextField(null=True)
    logo = models.TextField(null=True)
    industry_or_category = models.CharField(max_length=255, null=True)
    sub_category = models.CharField(max_length=255, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = FrameworkModelManager()

    class Meta:
        unique_together = ('name', 'site_name', 'link')

    def save(self, *args, **kwargs):
        """
        Overrides the save method to update the 'updated_at' field with the current date.
        """
        self.updated_at = datetime.date.today()
        super(Framework, self).save(*args, **kwargs)


class Cpv(models.Model):
    """
    Model representing a CPV code associated with a framework.

    Fields:
        code (IntegerField, optional): The CPV code. Defaults to None.
        framework (ForeignKey): The framework associated with the CPV code.
    """

    code = models.IntegerField(null=True)
    framework = models.ForeignKey(Framework, related_name='cpvs', on_delete=models.SET_NULL, null=True)


class Document(models.Model):
    """
    Model representing a document associated with a framework.

    Fields:
        name (TextField, optional): The name of the document. Defaults to None.
        link (TextField, optional): The link associated with the document. Defaults to None.
        is_available (BooleanField): Indicates if the document is available. Defaults to True.
        framework (ForeignKey): The framework associated with the document.

    Meta:
        unique_together = ('name', 'framework')
    """

    name = models.TextField(null=True)
    link = models.TextField(null=True)
    is_available = models.BooleanField(default=True)
    framework = models.ForeignKey(Framework, related_name='documents', on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('name', 'framework')


class LOT(models.Model):
    """
    Model representing a lot associated with a framework.

    Fields:
        name (TextField, optional): The name of the lot. Defaults to None.
        description (TextField, optional): The description of the lot. Defaults to None.
        framework (ForeignKey): The framework associated with the lot.
    """

    name = models.TextField(null=True)
    description = models.TextField(null=True)
    framework = models.ForeignKey(Framework, related_name='lots', on_delete=models.SET_NULL, null=True)


class Supplier(models.Model):
    """
    Model representing a supplier associated with a framework.

    Fields:
        name (TextField, optional): The name of the supplier. Defaults to None.
        link (TextField, optional): The link associated with the supplier. Defaults to None.
        is_available (BooleanField): Indicates if the supplier is available. Defaults to True.
        framework (ForeignKey): The framework associated with the supplier.

    Meta:
        unique_together = ('name', 'framework')
    """

    name = models.TextField(null=True)
    link = models.TextField(null=True)
    is_available = models.BooleanField(default=True)
    framework = models.ForeignKey(Framework, related_name='suppliers', on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('name', 'framework')


class FrameworkValue(models.Model):
    """
    Model representing the values used in the 'Search By Value' drop-down.

    Fields:
        value (CharField): The value for the drop-down.
        minimum_value (IntegerField, optional): The minimum value associated with the drop-down value. Defaults to None.
        maximum_value (IntegerField, optional): The maximum value associated with the drop-down value. Defaults to None.

    Methods:
        get_values(): Retrieves all the values from the FrameworkValue objects.
    """

    value = models.CharField(max_length=255)
    minimum_value = models.IntegerField(null=True)
    maximum_value = models.IntegerField(null=True)

    @classmethod
    def get_values(cls):
        """
        Retrieves all the values from the FrameworkValue objects.

        Returns:
            QuerySet: The queryset of FrameworkValue values.
        """
        return cls.objects.values_list('value', flat=True)

    def __str__(self):
        return self.value


class Preference(models.Model):
    """
    Model representing the user preferences for a framework.

    Fields:
        user (ForeignKey): The user associated with the preference.
        framework (ForeignKey): The framework associated with the preference.

    Meta:
        unique_together = ('user', 'framework')
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE, related_name='preferences')

    class Meta:
        unique_together = ('user', 'framework')

