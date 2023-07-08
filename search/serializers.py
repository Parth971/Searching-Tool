from rest_framework import serializers

from accounts.models import User
from search.constants import QUERY_TYPE_CHOICE_BY_VALUE, QUERY_TYPE_CHOICES, QUERY_TYPE_CHOICE_SEARCH_ALL, \
    INVALID_CPV_CODE
from search.models import FrameworkValue, Framework, Preference
from search.utils import get_model_object


class QueryByNameSerializer(serializers.Serializer):
    """
    Serializer for querying frameworks by name.

    Attributes:
        name (str): The name of the framework.
    """
    name = serializers.CharField()


class QueryByNumberSerializer(serializers.Serializer):
    """
    Serializer for querying frameworks by number.

    Attributes:
        number (str): The number of the framework.
    """
    number = serializers.CharField()


class CustomDateField(serializers.DateField):
    """
    Custom date field serializer.

    This serializer allows an empty string as a valid value for a date field.

    Example:
        start_date = CustomDateField(required=False, allow_null=True)
    """
    def to_internal_value(self, value):
        return None if value == '' else super().to_internal_value(value)


class FilterSerializer(serializers.Serializer):
    """
    Serializer for filtering frameworks.

    Attributes:
        cpv_code (str): The CPV code for filtering.
        industry_category_type (str): The industry category type for filtering.
        sub_category (str): The sub-category for filtering.
        start_date (date): The start date for filtering.
        end_date (date): The end date for filtering.
    """
    cpv_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    industry_category_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    sub_category = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    start_date = CustomDateField(required=False, allow_null=True)
    end_date = CustomDateField(required=False, allow_null=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        cpv_code = attrs.get('cpv_code')
        if cpv_code:
            try:
                int(cpv_code)
            except ValueError as e:
                raise serializers.ValidationError({'cpv_code': INVALID_CPV_CODE}) from e
        return attrs


class FrameworkDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for framework details.

    This serializer includes specific fields from the Framework model.
    """
    class Meta:
        model = Framework
        fields = ['id', 'name', 'lot_number', 'industry_or_category', 'sub_category', 'description', 'start_date',
                  'end_date']


class PreferencesSerializer(serializers.Serializer):
    """
    Serializer for user preferences.

    Attributes:
        user (int): The ID of the user.
        framework_id (int): The ID of the framework.

    Raises:
        serializers.ValidationError: If the preference already exists.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    framework_id = serializers.PrimaryKeyRelatedField(queryset=Framework.objects.all())

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = attrs.get('user')
        framework = attrs.get('framework_id')

        if get_model_object(model_class=Preference, query={'user': user, 'framework': framework}):
            raise serializers.ValidationError('Preference already added')

        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        framework = validated_data.get('framework_id')
        return Preference.objects.create(user=user, framework=framework)


class InquirySerializer(serializers.Serializer):
    """
    Serializer for inquiries.

    Attributes:
        inquiry_description (str): The description of the inquiry.
        framework_id (int): The ID of the framework.
    """

    inquiry_description = serializers.CharField()
    framework_id = serializers.PrimaryKeyRelatedField(queryset=Framework.objects.all())

    def get_email_context(self):
        return {
            'message': self.validated_data.get('inquiry_description'),
            'framework': self.validated_data.get('framework_id')
        }


class QueryValueSerializer(serializers.Serializer):
    """
    Serializer for querying frameworks by value.

    Attributes:
        value (str): The value for filtering.
        preference_frameworks (list): The list of framework names for filtering.

    Raises:
        serializers.ValidationError: If the value or framework names are invalid.
    """
    value = serializers.CharField(allow_blank=True, required=False)
    preference_frameworks = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    def validate(self, attrs):
        query_type = self.parent.initial_data.get('query_type')

        if not query_type:
            raise serializers.ValidationError({'query_type': 'query_type value not valid'})

        attrs = super().validate(attrs)

        if (
                query_type == QUERY_TYPE_CHOICE_BY_VALUE and
                not FrameworkValue.objects.filter(
                    value=attrs.get('value')
                ).exists()
        ):
            raise serializers.ValidationError({'value': 'Invalid value'})

        if query_type == QUERY_TYPE_CHOICE_SEARCH_ALL:
            preference_frameworks = Preference.objects.filter(user=self.context['request'].user).values_list(
                'framework__name', flat=True
            )
            for framework_name in attrs.get('preference_frameworks', []):
                if framework_name not in preference_frameworks:
                    raise serializers.ValidationError({'preference_frameworks': f'{framework_name} is not valid'})

        return attrs


class FrameworkFullQuerySerializer(serializers.Serializer):
    """
    Serializer for full framework queries.

    Attributes:
        query_type (str): The type of query.
        query (QueryValueSerializer): The query value serializer.
        filter (FilterSerializer): The filter serializer.
    """
    query_type = serializers.ChoiceField(choices=QUERY_TYPE_CHOICES)
    query = QueryValueSerializer()
    filter = FilterSerializer(default=FilterSerializer().data)


class AdminFrameworkQuerySerializer(serializers.Serializer):
    """
    Serializer for admin framework queries.

    Attributes:
        frameworks (list): The list of framework names for filtering.
        industry_category_types (list): The list of industry category types for filtering.
        sub_categories (list): The list of sub-categories for filtering.
        start_date (date): The start date for filtering.
        end_date (date): The end date for filtering.

    Raises:
        serializers.ValidationError: If the start_date and end_date are not provided together.
    """
    frameworks = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    industry_category_types = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    sub_categories = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    start_date = CustomDateField(required=False, allow_null=True)
    end_date = CustomDateField(required=False, allow_null=True)

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if (not start_date and end_date) or (start_date and not end_date):
            raise serializers.ValidationError("Both start_date and end_date should be provided.")

        return attrs


class IndustryTypeSerializers(serializers.Serializer):
    """
    Serializer for industry types.

    Attributes:
        industry_types (list): The list of industry types.

    Raises:
        serializers.ValidationError: If any industry type is not valid.
    """
    industry_types = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    def validate(self, attrs):
        industry_types = attrs.get('industry_types', [])

        industry_types_db = Framework.objects.values_list('industry_or_category', flat=True).distinct()
        for industry_type in industry_types:
            if industry_type not in industry_types_db:
                raise serializers.ValidationError({'industry_types': f'{industry_type} is not Valid Industry type'})

        return attrs
